"""블록 하나에 대한 세그먼트 추천: 규칙 실행 + 병합 + primary 선택."""

from typing import Any

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    BlockSegmentRecommendation,
    SegmentCandidate,
)

from document_parsing_engine.domain.segment.aggregation import (
    merge_candidates,
    select_primary_segment,
)


def recommend_for_block(
    *,
    doc_type: str,
    doc_dict: dict[str, Any],
    document_definition: DocumentSegmentDefinition,
    block: Any,
    rules: list[Any],
    primary_threshold: float = 0.50,
) -> BlockSegmentRecommendation:
    """규칙 실행 → 후보 필터/병합 → primary 선택 → BlockSegmentRecommendation 반환."""
    raw_candidates: list[SegmentCandidate] = []
    for rule in rules:
        if not rule.supports(
            doc_type=doc_type,
            document_definition=document_definition,
            block=block,
        ):
            continue
        raw_candidates.extend(
            rule.score(
                doc_type=doc_type,
                doc_dict=doc_dict,
                document_definition=document_definition,
                block=block,
            )
        )
    allowed_segments = {s.name for s in document_definition.segments}
    raw_candidates = [c for c in raw_candidates if c.segment_name in allowed_segments]
    merged = merge_candidates(raw_candidates)
    primary = select_primary_segment(merged, primary_threshold)

    block_ref = getattr(block, "ref", "")
    label = getattr(block, "label", None)
    content_type = getattr(block, "content_type", "")

    return BlockSegmentRecommendation(
        block_ref=block_ref,
        label=label,
        content_type=content_type,
        primary_segment=primary,
        candidates=merged,
    )
