from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.tasks import router as tasks_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Learning material organizer and revision content generator.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)


@app.on_event("startup")
def on_startup() -> None:
    settings.ensure_storage_dirs()
    Base.metadata.create_all(bind=engine)
