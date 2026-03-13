from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class TaskStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class OutputType(str, enum.Enum):
    OUTLINE = "outline"
    CHAPTER_SUMMARY = "chapter_summary"
    KEY_POINTS = "key_points"
    QUIZ = "quiz"
    FLASHCARDS = "flashcards"


class StudyTask(Base):
    __tablename__ = "study_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.UPLOADED, nullable=False)
    source_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    source_files: Mapped[list["SourceFile"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="SourceFile.created_at",
    )
    segments: Mapped[list["ContentSegment"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="ContentSegment.segment_order",
    )
    outputs: Mapped[list["GeneratedOutput"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="GeneratedOutput.created_at",
    )


class SourceFile(Base):
    __tablename__ = "source_files"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(ForeignKey("study_tasks.id", ondelete="CASCADE"), index=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(32))
    mime_type: Mapped[str] = mapped_column(String(255))
    size_bytes: Mapped[int] = mapped_column(Integer)
    storage_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    task: Mapped[StudyTask] = relationship(back_populates="source_files")
    segments: Mapped[list["ContentSegment"]] = relationship(back_populates="source_file")


class ContentSegment(Base):
    __tablename__ = "content_segments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(ForeignKey("study_tasks.id", ondelete="CASCADE"), index=True)
    source_file_id: Mapped[str] = mapped_column(ForeignKey("source_files.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String(32))
    source_label: Mapped[str] = mapped_column(String(255))
    segment_order: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    task: Mapped[StudyTask] = relationship(back_populates="segments")
    source_file: Mapped[SourceFile] = relationship(back_populates="segments")


class GeneratedOutput(Base):
    __tablename__ = "generated_outputs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id: Mapped[str] = mapped_column(ForeignKey("study_tasks.id", ondelete="CASCADE"), index=True)
    output_type: Mapped[OutputType] = mapped_column(Enum(OutputType), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    content_markdown: Mapped[str] = mapped_column(Text)
    content_json: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    generated_by: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    task: Mapped[StudyTask] = relationship(back_populates="outputs")
