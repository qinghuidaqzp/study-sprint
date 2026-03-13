from __future__ import annotations

from pathlib import Path

from openai import OpenAI

from app.core.config import settings
from app.services.parsers.base import ParsedSegmentPayload
from app.utils.text import clean_text


def _parse_with_local_whisper(path: Path) -> list[ParsedSegmentPayload]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Local audio transcription requires the 'faster-whisper' package. Install dependencies or switch to the OpenAI-compatible transcription backend."
        ) from exc

    model = WhisperModel(settings.whisper_model_size, device="cpu", compute_type="int8")
    segments_iter, _ = model.transcribe(str(path), beam_size=5, vad_filter=True)

    segments: list[ParsedSegmentPayload] = []
    for index, item in enumerate(segments_iter, start=1):
        text = clean_text(item.text)
        if not text:
            continue
        segments.append(
            ParsedSegmentPayload(
                source_type="audio",
                source_label=f"音频 {item.start:.0f}s - {item.end:.0f}s",
                segment_order=index,
                content=text,
                metadata_json={"start": item.start, "end": item.end},
            )
        )
    return segments


def _parse_with_openai_compatible(path: Path) -> list[ParsedSegmentPayload]:
    if not settings.ai_api_key:
        raise RuntimeError("AI_API_KEY is required for the OpenAI-compatible transcription backend.")

    client = OpenAI(api_key=settings.ai_api_key, base_url=settings.ai_base_url)
    with path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
        )

    segments: list[ParsedSegmentPayload] = []
    verbose_segments = getattr(transcript, "segments", None) or []
    if verbose_segments:
        for index, item in enumerate(verbose_segments, start=1):
            text = clean_text(item["text"] if isinstance(item, dict) else item.text)
            if not text:
                continue
            start = item["start"] if isinstance(item, dict) else item.start
            end = item["end"] if isinstance(item, dict) else item.end
            segments.append(
                ParsedSegmentPayload(
                    source_type="audio",
                    source_label=f"音频 {start:.0f}s - {end:.0f}s",
                    segment_order=index,
                    content=text,
                    metadata_json={"start": start, "end": end},
                )
            )
    elif getattr(transcript, "text", None):
        segments.append(
            ParsedSegmentPayload(
                source_type="audio",
                source_label="音频全文",
                segment_order=1,
                content=clean_text(transcript.text),
                metadata_json={"backend": "openai-compatible"},
            )
        )
    return segments


def parse_audio_file(path: Path) -> list[ParsedSegmentPayload]:
    if settings.whisper_backend.lower() == "openai":
        return _parse_with_openai_compatible(path)
    return _parse_with_local_whisper(path)
