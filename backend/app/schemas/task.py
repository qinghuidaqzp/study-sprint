from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.task import OutputType, TaskStatus


class SourceFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    original_name: str
    stored_name: str
    file_type: str
    mime_type: str
    size_bytes: int
    storage_path: str
    created_at: datetime


class ContentSegmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_type: str
    source_label: str
    segment_order: int
    content: str
    metadata_json: dict[str, Any]
    created_at: datetime


class GeneratedOutputRead(BaseModel):
    id: str
    output_type: OutputType
    title: str
    content_markdown: str
    content_json: dict[str, Any] | list[Any] | None = None
    created_at: datetime


class StudyTaskCreateResponse(BaseModel):
    id: str
    title: str
    status: TaskStatus
    message: str


class StudyTaskSummary(BaseModel):
    id: str
    title: str
    status: TaskStatus
    source_types: list[str]
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    file_count: int
    segment_count: int
    output_count: int


class StudyTaskDetail(StudyTaskSummary):
    files: list[SourceFileRead]
    segments_preview: list[ContentSegmentRead]
    outputs: dict[str, GeneratedOutputRead]
