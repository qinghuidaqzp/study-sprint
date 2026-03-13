from __future__ import annotations

from pathlib import Path

import fitz

from app.services.parsers.base import ParsedSegmentPayload
from app.utils.text import clean_text, split_text_blocks


def parse_pdf_file(path: Path) -> list[ParsedSegmentPayload]:
    document = fitz.open(path)
    segments: list[ParsedSegmentPayload] = []
    order = 1
    for page_index in range(document.page_count):
        page = document.load_page(page_index)
        page_text = clean_text(page.get_text("text"))
        if not page_text:
            continue
        blocks = split_text_blocks(page_text, min_length=30)
        for block in blocks:
            text = clean_text(block)
            if not text:
                continue
            segments.append(
                ParsedSegmentPayload(
                    source_type="pdf",
                    source_label=f"PDF 第 {page_index + 1} 页",
                    segment_order=order,
                    content=text,
                    metadata_json={"page": page_index + 1},
                )
            )
            order += 1
    document.close()
    return segments
