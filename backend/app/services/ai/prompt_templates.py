from __future__ import annotations

from dataclasses import dataclass

from app.models.task import OutputType
from app.services.parsers.base import ParsedSegmentPayload


BASE_SYSTEM_PROMPT = """
你是一个专注考试复习场景的学习资料整理助手。
你的目标不是泛泛总结，而是把原始材料整理成真正适合学生考前复习的内容。

必须遵守：
1. 优先保留原材料中的概念、定义、公式、流程、结论和因果关系。
2. 输出要层次清晰，适合快速浏览与背诵。
3. 不要写空泛套话，不要输出会议纪要口吻。
4. 如果材料不足以支撑判断，明确写出“基于现有材料推测”。
5. 所有输出都使用中文 Markdown。
""".strip()


@dataclass(frozen=True)
class PromptTemplate:
    output_type: OutputType
    title: str
    instruction: str


PROMPT_TEMPLATES = [
    PromptTemplate(
        output_type=OutputType.OUTLINE,
        title="复习提纲",
        instruction="""
请把材料整理为考前复习提纲：
- 按章节/主题分层
- 尽量使用二级、三级标题
- 每个主题下保留关键知识点
- 必要时附上来源提示，例如“来源：PDF 第 3 页”
""".strip(),
    ),
    PromptTemplate(
        output_type=OutputType.CHAPTER_SUMMARY,
        title="章节总结",
        instruction="""
请把材料整理为章节总结：
- 以“章节/主题”分组
- 每章 3 到 6 条简洁总结
- 强调考试时最容易被问到的核心内容
""".strip(),
    ),
    PromptTemplate(
        output_type=OutputType.KEY_POINTS,
        title="高频考点",
        instruction="""
请抽取高频考点：
- 优先提取定义、公式、结论、流程、对比点、易错点
- 用列表形式输出
- 每条尽量短、准、能背
- 对于不够确定的部分，明确标注“基于现有材料推测”
""".strip(),
    ),
    PromptTemplate(
        output_type=OutputType.QUIZ,
        title="练习题",
        instruction="""
请生成贴近材料的练习题：
- 至少 4 道选择题和 3 道简答题
- 每道题都给参考答案
- 选择题要有 4 个选项
- 不要脱离材料随意发挥
""".strip(),
    ),
    PromptTemplate(
        output_type=OutputType.FLASHCARDS,
        title="速记卡片",
        instruction="""
请生成适合背诵的 Q/A 卡片：
- 至少 10 组
- 每组尽量简洁
- 问题聚焦一个知识点
- 答案控制在 1 到 3 句
""".strip(),
    ),
]


def build_material_context(segments: list[ParsedSegmentPayload], max_chars: int = 14000) -> str:
    ordered = sorted(segments, key=lambda item: item.segment_order)
    lines: list[str] = []
    total = 0
    for index, segment in enumerate(ordered, start=1):
        chunk = f"[{index}] 来源：{segment.source_label}\n{segment.content}\n"
        if total + len(chunk) > max_chars:
            break
        lines.append(chunk)
        total += len(chunk)
    return "\n".join(lines)
