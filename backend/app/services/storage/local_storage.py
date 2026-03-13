from __future__ import annotations

import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


SUPPORTED_EXTENSIONS = {".pdf", ".pptx", ".txt", ".md", ".mp3", ".wav", ".m4a"}


@dataclass
class StoredUpload:
    original_name: str
    stored_name: str
    file_type: str
    mime_type: str
    size_bytes: int
    storage_path: str


def _infer_file_type(suffix: str) -> str:
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".pptx":
        return "pptx"
    if suffix in {".txt", ".md"}:
        return "text"
    if suffix in {".mp3", ".wav", ".m4a"}:
        return "audio"
    return "unknown"


def persist_upload(upload: UploadFile) -> StoredUpload:
    settings.ensure_storage_dirs()
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format.")

    stored_name = f"{uuid.uuid4()}{suffix}"
    destination = settings.upload_dir / stored_name
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    size_bytes = destination.stat().st_size
    if size_bytes > settings.max_upload_size_mb * 1024 * 1024:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File '{upload.filename}' exceeds the {settings.max_upload_size_mb}MB limit.",
        )

    return StoredUpload(
        original_name=upload.filename or stored_name,
        stored_name=stored_name,
        file_type=_infer_file_type(suffix),
        mime_type=upload.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        storage_path=str(destination),
    )
