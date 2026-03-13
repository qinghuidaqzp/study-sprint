from __future__ import annotations

import re
from pathlib import Path

from app.core.config import settings
from app.models.task import StudyTask


def _slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower() or "task"


def export_task_to_markdown(task: StudyTask) -> Path:
    settings.ensure_storage_dirs()
    file_path = settings.export_dir / f"{_slugify(task.title)}-{task.id}.md"

    lines = [f"# {task.title}", "", f"- 任务状态：{task.status.value}", f"- 文件数量：{len(task.source_files)}", ""]

    lines.extend(["## 原始解析文本概览", ""])
    for segment in sorted(task.segments, key=lambda item: item.segment_order):
        lines.extend([f"### {segment.source_label}", segment.content, ""])

    for output in sorted(task.outputs, key=lambda item: item.output_type.value):
        lines.extend([output.content_markdown, ""])

    file_path.write_text("\n".join(lines).strip(), encoding="utf-8")
    return file_path
