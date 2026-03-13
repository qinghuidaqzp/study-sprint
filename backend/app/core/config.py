from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Study Sprint Generator"
    app_env: str = "development"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/study_sprint"
    storage_root: Path = BASE_DIR / "storage"
    upload_dir_name: str = "uploads"
    export_dir_name: str = "exports"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    max_upload_size_mb: int = 200

    ai_provider: str = "mock"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_model: str = "gpt-4.1-mini"

    whisper_backend: str = "local"
    whisper_model_size: str = "base"

    @property
    def upload_dir(self) -> Path:
        return self.storage_root / self.upload_dir_name

    @property
    def export_dir(self) -> Path:
        return self.storage_root / self.export_dir_name

    def ensure_storage_dirs(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
