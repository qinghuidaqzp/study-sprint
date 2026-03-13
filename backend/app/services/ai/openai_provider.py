from __future__ import annotations

from openai import OpenAI

from app.core.config import settings
from app.services.ai.base import BaseAIProvider, GeneratedBundleItem
from app.services.ai.prompt_templates import BASE_SYSTEM_PROMPT, PROMPT_TEMPLATES, build_material_context
from app.services.parsers.base import ParsedSegmentPayload


class OpenAICompatibleProvider(BaseAIProvider):
    provider_name = "openai-compatible"

    def __init__(self) -> None:
        if not settings.ai_api_key:
            raise RuntimeError("AI_API_KEY is required when AI_PROVIDER is not 'mock'.")
        self.client = OpenAI(api_key=settings.ai_api_key, base_url=settings.ai_base_url)

    def generate_outputs(self, title: str, segments: list[ParsedSegmentPayload]) -> list[GeneratedBundleItem]:
        context = build_material_context(segments)
        items: list[GeneratedBundleItem] = []
        for template in PROMPT_TEMPLATES:
            prompt = f"""
任务标题：{title}

请根据以下材料生成《{template.title}》：
{template.instruction}

材料如下：
{context}

请直接输出最终 Markdown，不要附加解释。
""".strip()
            response = self.client.chat.completions.create(
                model=settings.ai_model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": BASE_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            content = response.choices[0].message.content or ""
            items.append(
                GeneratedBundleItem(
                    output_type=template.output_type,
                    title=template.title,
                    content_markdown=content.strip(),
                )
            )
        return items
