from __future__ import annotations

from pathlib import Path

from app.services.parsers.base import ParsedSegmentPayload
from app.utils.text import clean_text, split_text_blocks


def parse_text_file(path: Path, source_label_prefix: str = "文本") -> list[ParsedSegmentPayload]:
    raw_text = path.read_text(encoding="utf-8", errors="ignore")
    blocks = split_text_blocks(raw_text)
    segments: list[ParsedSegmentPayload] = []
    for index, block in enumerate(blocks, start=1):
        text = clean_text(block)
        if not text:
            continue
        segments.append(
            ParsedSegmentPayload(
                source_type="text",
                source_label=f"{source_label_prefix} 第 {index} 段",
                segment_order=index,
                content=text,
                metadata_json={"block_index": index},
            )
        )
    return segments
