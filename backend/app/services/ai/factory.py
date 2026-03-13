from __future__ import annotations

from app.core.config import settings
from app.services.ai.base import BaseAIProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.ai.openai_provider import OpenAICompatibleProvider


def get_ai_provider() -> BaseAIProvider:
    if settings.ai_provider.lower() == "mock":
        return MockAIProvider()
    return OpenAICompatibleProvider()
