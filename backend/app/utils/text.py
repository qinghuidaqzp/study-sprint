from __future__ import annotations

import re
from itertools import islice


def clean_text(value: str) -> str:
    text = value.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_text_blocks(value: str, min_length: int = 20) -> list[str]:
    normalized = clean_text(value)
    if not normalized:
        return []
    blocks = re.split(r"\n\s*\n", normalized)
    candidate_blocks = [block.strip() for block in blocks if len(block.strip()) >= min_length]
    if candidate_blocks:
        return candidate_blocks
    return [normalized]


def split_sentences(value: str) -> list[str]:
    normalized = clean_text(value)
    if not normalized:
        return []
    sentences = re.split(r"(?<=[。！？.!?；;])\s*", normalized)
    cleaned = [sentence.strip(" -•") for sentence in sentences if len(sentence.strip()) > 8]
    return cleaned


def extract_candidate_points(contents: list[str], limit: int = 10) -> list[str]:
    priority_keywords = ["定义", "公式", "结论", "原理", "步骤", "流程", "特点", "区别", "方法", "条件"]
    ranked: list[str] = []
    fallback: list[str] = []
    seen: set[str] = set()
    for content in contents:
        for sentence in split_sentences(content):
            short = sentence[:120]
            if short in seen:
                continue
            seen.add(short)
            if any(keyword in short for keyword in priority_keywords):
                ranked.append(short)
            else:
                fallback.append(short)
    combined = list(islice(ranked + fallback, limit))
    return combined or ["基于现有材料，建议优先复习核心概念、关键流程和高频结论。"]


def build_flashcard_pairs(points: list[str]) -> list[dict[str, str]]:
    pairs: list[dict[str, str]] = []
    for point in points[:10]:
        prompt = point[:26]
        pairs.append(
            {
                "question": f"{prompt} 的核心内容是什么？",
                "answer": point,
            }
        )
    if not pairs:
        pairs.append(
            {
                "question": "这份材料最应该先记住什么？",
                "answer": "先记住核心概念、关键步骤和最终结论。",
            }
        )
    return pairs
