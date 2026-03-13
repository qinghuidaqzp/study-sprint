from __future__ import annotations

from collections import OrderedDict
from itertools import islice

from app.models.task import OutputType
from app.services.ai.base import BaseAIProvider, GeneratedBundleItem
from app.services.parsers.base import ParsedSegmentPayload
from app.utils.text import build_flashcard_pairs, extract_candidate_points, split_sentences


class MockAIProvider(BaseAIProvider):
    provider_name = "mock"

    def generate_outputs(self, title: str, segments: list[ParsedSegmentPayload]) -> list[GeneratedBundleItem]:
        grouped = self._group_segments(segments)
        key_points = extract_candidate_points([segment.content for segment in segments], limit=12)
        flashcards = build_flashcard_pairs(key_points)

        return [
            GeneratedBundleItem(
                output_type=OutputType.OUTLINE,
                title="复习提纲",
                content_markdown=self._build_outline(title, grouped),
            ),
            GeneratedBundleItem(
                output_type=OutputType.CHAPTER_SUMMARY,
                title="章节总结",
                content_markdown=self._build_chapter_summary(grouped),
            ),
            GeneratedBundleItem(
                output_type=OutputType.KEY_POINTS,
                title="高频考点",
                content_markdown=self._build_key_points(key_points, len(segments) < 5),
                content_json={"points": key_points},
            ),
            GeneratedBundleItem(
                output_type=OutputType.QUIZ,
                title="练习题",
                content_markdown=self._build_quiz(key_points),
            ),
            GeneratedBundleItem(
                output_type=OutputType.FLASHCARDS,
                title="速记卡片",
                content_markdown=self._build_flashcards(flashcards),
                content_json=flashcards,
            ),
        ]

    def _group_segments(self, segments: list[ParsedSegmentPayload]) -> OrderedDict[str, list[str]]:
        grouped: OrderedDict[str, list[str]] = OrderedDict()
        for segment in sorted(segments, key=lambda item: item.segment_order):
            grouped.setdefault(segment.source_label, []).append(segment.content)
        return grouped

    def _build_outline(self, title: str, grouped: OrderedDict[str, list[str]]) -> str:
        lines = [f"# {title} 复习提纲", "", "> 以下内容基于现有材料自动整理，适合作为考前速览。", ""]
        for index, (label, parts) in enumerate(grouped.items(), start=1):
            lines.append(f"## 主题 {index}：{label}")
            sentences = split_sentences(" ".join(parts))
            for sentence in islice(sentences, 0, 4):
                lines.append(f"- {sentence}")
            lines.append("")
        return "\n".join(lines).strip()

    def _build_chapter_summary(self, grouped: OrderedDict[str, list[str]]) -> str:
        lines = ["# 章节总结", ""]
        for index, (label, parts) in enumerate(grouped.items(), start=1):
            lines.append(f"## 章节 {index}：{label}")
            sentences = split_sentences(" ".join(parts))
            for sentence in islice(sentences, 0, 3):
                lines.append(f"- {sentence}")
            if len(sentences) < 2:
                lines.append("- 基于现有材料推测：本章节更适合与其他页面或段落合并理解。")
            lines.append("")
        return "\n".join(lines).strip()

    def _build_key_points(self, key_points: list[str], add_inference_note: bool) -> str:
        lines = ["# 高频考点", ""]
        if add_inference_note:
            lines.extend(["> 基于现有材料推测：原始材料较少，以下考点中部分为从上下文归纳得到。", ""])
        for index, point in enumerate(key_points, start=1):
            lines.append(f"{index}. {point}")
        return "\n".join(lines).strip()

    def _build_quiz(self, key_points: list[str]) -> str:
        points = key_points[:7] or ["请根据材料补充核心知识点。"]
        lines = ["# 练习题", "", "## 选择题", ""]
        for index, point in enumerate(points[:4], start=1):
            topic = point[:28]
            lines.extend(
                [
                    f"{index}. 关于“{topic}”，哪项最符合材料内容？",
                    "A. 它是材料中的核心概念或流程，需要重点掌握",
                    "B. 它只是与主题无关的背景信息",
                    "C. 材料明确表示考试中无需关注",
                    "D. 材料认为它与其他概念完全没有联系",
                    "",
                    "参考答案：A",
                    f"解析：材料围绕“{topic}”展开，说明其属于应重点复习的知识点。",
                    "",
                ]
            )

        lines.extend(["## 简答题", ""])
        for index, point in enumerate(points[4:7], start=1):
            lines.extend(
                [
                    f"{index}. 请简要说明“{point[:30]}”的核心内容，并结合材料指出其重要性。",
                    "参考答案：应从定义、关键步骤、使用条件或结论展开，并结合原文中的对应内容作答。",
                    "",
                ]
            )
        return "\n".join(lines).strip()

    def _build_flashcards(self, flashcards: list[dict[str, str]]) -> str:
        lines = ["# 速记卡片", ""]
        for index, item in enumerate(flashcards[:10], start=1):
            lines.extend(
                [
                    f"## 卡片 {index}",
                    f"Q: {item['question']}",
                    f"A: {item['answer']}",
                    "",
                ]
            )
        return "\n".join(lines).strip()
