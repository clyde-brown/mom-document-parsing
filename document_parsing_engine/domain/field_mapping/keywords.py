"""doc_type → 세그먼트별 필드 키워드 매핑 (프롬프트 변수용)."""

from __future__ import annotations

from typing import Any

from document_parsing_engine.domain.presets.segment_definitions import (
    get_segment_definition,
)


def build_segment_field_keywords(doc_type: str) -> dict[str, Any]:
    """doc_type에 맞는 세그먼트 정의에서 필드별 키워드 매핑을 만든다.
    Returns: { "quotation_meta": { "document_key": [...], ... }, "items": { "rows": {...}, "totals": {...} }, "remarks": {...} }
    """
    definition = get_segment_definition(doc_type)
    out: dict[str, Any] = {}
    for seg in definition.segments:
        out[seg.name] = {}
        for f in seg.fields:
            kw = list(getattr(f.keyword_def, "keywords", ()) or ())
            if not getattr(f, "children", None):
                out[seg.name][f.name] = kw
            else:
                out[seg.name][f.name] = {"keywords": kw}
                for c in f.children:
                    out[seg.name][f.name][c.name] = list(
                        getattr(c.keyword_def, "keywords", ()) or ()
                    )
    return out
