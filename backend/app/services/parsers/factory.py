from __future__ import annotations

from pathlib import Path

from app.services.parsers.audio_parser import parse_audio_file
from app.services.parsers.base import ParsedSegmentPayload
from app.services.parsers.pdf_parser import parse_pdf_file
from app.services.parsers.pptx_parser import parse_pptx_file
from app.services.parsers.text_parser import parse_text_file


def parse_file(path: Path, file_type: str) -> list[ParsedSegmentPayload]:
    if file_type == "pdf":
        return parse_pdf_file(path)
    if file_type == "pptx":
        return parse_pptx_file(path)
    if file_type == "audio":
        return parse_audio_file(path)
    if file_type == "text":
        return parse_text_file(path)
    raise ValueError(f"Unsupported parser file_type: {file_type}")
