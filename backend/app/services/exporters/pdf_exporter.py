from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.core.config import settings
from app.models.task import StudyTask


def _slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower() or "task"


def export_task_to_pdf(task: StudyTask) -> Path:
    settings.ensure_storage_dirs()
    output_path = settings.export_dir / f"{_slugify(task.title)}-{task.id}.pdf"
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCN",
        parent=styles["Title"],
        fontName="STSong-Light",
        fontSize=18,
        leading=24,
    )
    body_style = ParagraphStyle(
        "BodyCN",
        parent=styles["BodyText"],
        fontName="STSong-Light",
        fontSize=10.5,
        leading=16,
    )

    story = [
        Paragraph(task.title, title_style),
        Spacer(1, 6 * mm),
        Paragraph(f"任务状态：{task.status.value}", body_style),
        Spacer(1, 4 * mm),
    ]

    for output in sorted(task.outputs, key=lambda item: item.output_type.value):
        story.append(Paragraph(output.title, title_style))
        story.append(Spacer(1, 3 * mm))
        for line in output.content_markdown.splitlines():
            if not line.strip():
                story.append(Spacer(1, 2 * mm))
                continue
            safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe_line, body_style))
        story.append(Spacer(1, 5 * mm))

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
    )
    document.build(story)
    return output_path
