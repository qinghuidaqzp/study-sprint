from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParsedSegmentPayload:
    source_type: str
    source_label: str
    segment_order: int
    content: str
    metadata_json: dict[str, Any] = field(default_factory=dict)
