from __future__ import annotations

from pathlib import Path
from typing import Iterable

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.db.session import get_db
from app.models.task import SourceFile, StudyTask
from app.schemas.task import ContentSegmentRead, StudyTaskCreateResponse, StudyTaskDetail, StudyTaskSummary
from app.services.exporters.markdown_exporter import export_task_to_markdown
from app.services.exporters.pdf_exporter import export_task_to_pdf
from app.services.storage.local_storage import SUPPORTED_EXTENSIONS, persist_upload
from app.services.task_processor import process_task


router = APIRouter(tags=["tasks"])


def _load_task_or_404(db: Session, task_id: str) -> StudyTask:
    query = (
        select(StudyTask)
        .options(
            selectinload(StudyTask.source_files),
            selectinload(StudyTask.segments),
            selectinload(StudyTask.outputs),
        )
        .where(StudyTask.id == task_id)
    )
    task = db.execute(query).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task


def _build_task_summary(task: StudyTask) -> StudyTaskSummary:
    return StudyTaskSummary.model_validate(
        {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "source_types": task.source_types or [],
            "error_message": task.error_message,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "completed_at": task.completed_at,
            "file_count": len(task.source_files),
            "segment_count": len(task.segments),
            "output_count": len(task.outputs),
        }
    )


def _build_task_detail(task: StudyTask) -> StudyTaskDetail:
    sorted_segments = sorted(task.segments, key=lambda item: item.segment_order)
    outputs = {
        output.output_type.value: {
            "id": output.id,
            "output_type": output.output_type,
            "title": output.title,
            "content_markdown": output.content_markdown,
            "content_json": output.content_json,
            "created_at": output.created_at,
        }
        for output in sorted(task.outputs, key=lambda item: item.output_type.value)
    }
    return StudyTaskDetail.model_validate(
        {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "source_types": task.source_types or [],
            "error_message": task.error_message,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "completed_at": task.completed_at,
            "file_count": len(task.source_files),
            "segment_count": len(task.segments),
            "output_count": len(task.outputs),
            "files": task.source_files,
            "segments_preview": sorted_segments[:12],
            "outputs": outputs,
        }
    )


def _validate_filenames(files: Iterable[UploadFile]) -> None:
    for upload in files:
        suffix = Path(upload.filename or "").suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            allowed = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {suffix or 'unknown'}. Allowed: {allowed}",
            )


@router.post("/tasks", response_model=StudyTaskCreateResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
) -> StudyTaskCreateResponse:
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload at least one file.")
    _validate_filenames(files)

    clean_title = title.strip() or "Untitled task"
    task = StudyTask(title=clean_title, source_types=[])
    db.add(task)
    db.flush()

    source_types: set[str] = set()
    for upload in files:
        stored = persist_upload(upload)
        task.source_files.append(
            SourceFile(
                task_id=task.id,
                original_name=stored.original_name,
                stored_name=stored.stored_name,
                file_type=stored.file_type,
                mime_type=stored.mime_type,
                size_bytes=stored.size_bytes,
                storage_path=stored.storage_path,
            )
        )
        source_types.add(stored.file_type)

    task.source_types = sorted(source_types)
    db.commit()
    background_tasks.add_task(process_task, task.id)

    return StudyTaskCreateResponse(
        id=task.id,
        title=task.title,
        status=task.status,
        message="Files uploaded successfully. Processing started in the background.",
    )


@router.post("/tasks/{task_id}/process", response_model=StudyTaskCreateResponse)
def retry_process_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> StudyTaskCreateResponse:
    task = _load_task_or_404(db, task_id)
    background_tasks.add_task(process_task, task.id)
    return StudyTaskCreateResponse(
        id=task.id,
        title=task.title,
        status=task.status,
        message="Task reprocessing started.",
    )


@router.get("/tasks", response_model=list[StudyTaskSummary])
def list_tasks(db: Session = Depends(get_db)) -> list[StudyTaskSummary]:
    if not settings.history_enabled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History is disabled.")

    query = (
        select(StudyTask)
        .options(
            selectinload(StudyTask.source_files),
            selectinload(StudyTask.segments),
            selectinload(StudyTask.outputs),
        )
        .order_by(StudyTask.created_at.desc())
    )
    tasks = db.execute(query).scalars().all()
    return [_build_task_summary(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=StudyTaskDetail)
def get_task(task_id: str, db: Session = Depends(get_db)) -> StudyTaskDetail:
    task = _load_task_or_404(db, task_id)
    return _build_task_detail(task)


@router.get("/tasks/{task_id}/segments", response_model=list[ContentSegmentRead])
def get_task_segments(task_id: str, db: Session = Depends(get_db)) -> list[ContentSegmentRead]:
    task = _load_task_or_404(db, task_id)
    sorted_segments = sorted(task.segments, key=lambda item: item.segment_order)
    return [ContentSegmentRead.model_validate(segment) for segment in sorted_segments]


@router.get("/tasks/{task_id}/export/markdown")
def download_markdown(task_id: str, db: Session = Depends(get_db)) -> FileResponse:
    task = _load_task_or_404(db, task_id)
    output_path = export_task_to_markdown(task)
    return FileResponse(output_path, media_type="text/markdown", filename=output_path.name)


@router.get("/tasks/{task_id}/export/pdf")
def download_pdf(task_id: str, db: Session = Depends(get_db)) -> FileResponse:
    task = _load_task_or_404(db, task_id)
    output_path = export_task_to_pdf(task)
    return FileResponse(output_path, media_type="application/pdf", filename=output_path.name)