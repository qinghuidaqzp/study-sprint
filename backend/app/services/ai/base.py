from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.models.task import OutputType
from app.services.parsers.base import ParsedSegmentPayload


@dataclass
class GeneratedBundleItem:
    output_type: OutputType
    title: str
    content_markdown: str
    content_json: dict[str, Any] | list[Any] | None = None


class BaseAIProvider(ABC):
    provider_name: str

    @abstractmethod
    def generate_outputs(self, title: str, segments: list[ParsedSegmentPayload]) -> list[GeneratedBundleItem]:
        raise NotImplementedError
