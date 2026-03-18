"""정의 → 키워드 번들 생성 (규칙 점수용)."""

from typing import Iterable

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
    FieldDefinition,
)


def _walk_fields(
    fields: tuple[FieldDefinition, ...],
) -> Iterable[FieldDefinition]:
    for field_def in fields:
        yield field_def
        if field_def.children:
            yield from _walk_fields(field_def.children)


def _dedupe_keyword_pairs(
    pairs: list[tuple[str, float]],
) -> list[tuple[str, float]]:
    seen: set[str] = set()
    result: list[tuple[str, float]] = []
    for keyword, score in pairs:
        normalized = " ".join(keyword.strip().lower().split())
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append((keyword, score))
    return result


def build_segment_keyword_bundle(
    document_definition: DocumentSegmentDefinition,
) -> dict[str, dict[str, list[tuple[str, float]]]]:
    """DocumentSegmentDefinition → segment별 field/segment/title 키워드 번들."""
    result: dict[str, dict[str, list[tuple[str, float]]]] = {}
    for segment in document_definition.segments:
        field_keywords: list[tuple[str, float]] = []
        for field_def in _walk_fields(segment.fields):
            for keyword in field_def.keyword_def.keywords:
                if keyword:
                    field_keywords.append(
                        (str(keyword).strip(), float(field_def.keyword_def.boost_score))
                    )
        segment_boost = float(
            segment.metadata.get("segment_keyword_boost_score", 0.0) or 0.0
        )
        segment_keywords = [
            (str(k).strip(), segment_boost)
            for k in segment.metadata.get("segment_keywords", ())
            if k
        ]
        title_boost = float(segment.metadata.get("title_boost_score", 0.0) or 0.0)
        title_keywords = [
            (str(k).strip(), title_boost)
            for k in segment.metadata.get("title_keywords", ())
            if k
        ]
        result[segment.name] = {
            "field_keywords": _dedupe_keyword_pairs(field_keywords),
            "segment_keywords": _dedupe_keyword_pairs(segment_keywords),
            "title_keywords": _dedupe_keyword_pairs(title_keywords),
        }
    return result
