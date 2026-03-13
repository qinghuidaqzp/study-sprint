from __future__ import annotations

from pathlib import Path

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.db.session import SessionLocal
from app.models.task import ContentSegment, GeneratedOutput, StudyTask, TaskStatus, utcnow
from app.services.ai.factory import get_ai_provider
from app.services.parsers.factory import parse_file


def process_task(task_id: str) -> None:
    db = SessionLocal()
    try:
        task = (
            db.execute(
                select(StudyTask)
                .options(selectinload(StudyTask.source_files))
                .where(StudyTask.id == task_id)
            )
            .scalar_one()
        )
        task.status = TaskStatus.PARSING
        task.error_message = None
        task.completed_at = None
        db.commit()

        db.execute(delete(ContentSegment).where(ContentSegment.task_id == task.id))
        db.execute(delete(GeneratedOutput).where(GeneratedOutput.task_id == task.id))
        db.commit()

        all_segments = []
        global_order = 1
        for source_file in task.source_files:
            parsed_segments = parse_file(Path(source_file.storage_path), source_file.file_type)
            for segment in parsed_segments:
                db.add(
                    ContentSegment(
                        task_id=task.id,
                        source_file_id=source_file.id,
                        source_type=segment.source_type,
                        source_label=segment.source_label,
                        segment_order=global_order,
                        content=segment.content,
                        metadata_json=segment.metadata_json,
                    )
                )
                all_segments.append(segment)
                global_order += 1
        db.commit()

        if not all_segments:
            raise RuntimeError("No readable text was extracted from the uploaded materials.")

        task.status = TaskStatus.GENERATING
        db.commit()

        provider = get_ai_provider()
        outputs = provider.generate_outputs(task.title, all_segments)
        for item in outputs:
            db.add(
                GeneratedOutput(
                    task_id=task.id,
                    output_type=item.output_type,
                    title=item.title,
                    content_markdown=item.content_markdown,
                    content_json=item.content_json,
                    generated_by=provider.provider_name,
                )
            )

        task.status = TaskStatus.COMPLETED
        task.error_message = None
        task.completed_at = utcnow()
        db.commit()
    except Exception as exc:
        db.rollback()
        task = db.get(StudyTask, task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error_message = str(exc)
            task.completed_at = None
            db.commit()
    finally:
        db.close()
