"""세그먼트 매핑 결과(seg) + blocks → 세그먼트별 블록 데이터 dict."""

from __future__ import annotations

from typing import Any, Protocol

from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
)


class BlockLike(Protocol):
    ref: str
    label: str
    content_type: str
    content: Any


def build_segment_data(
    recommendation: LayoutSegmentMappingRecommendation,
    blocks: list[BlockLike],
) -> dict[str, list[dict[str, Any]]]:
    """segment_buckets 기준으로 세그먼트별 블록 리스트를 JSON 직렬화 가능한 dict로 반환.
    Returns: { segment_name: [ {"ref", "label", "content_type", "content"}, ... ], "_unmapped": [...] }
    """
    blocks_by_ref = {getattr(b, "ref", None): b for b in blocks if getattr(b, "ref", None)}
    out: dict[str, list[dict[str, Any]]] = {}
    for bucket in recommendation.segment_buckets:
        out[bucket.segment_name] = [
            _block_to_dict(blocks_by_ref[ref])
            for ref in bucket.block_refs
            if ref in blocks_by_ref
        ]
    out["_unmapped"] = [
        _block_to_dict(blocks_by_ref[ref])
        for ref in recommendation.unmapped_block_refs
        if ref in blocks_by_ref
    ]
    return out


def _block_to_dict(block: BlockLike | None) -> dict[str, Any]:
    if block is None:
        return {}
    return {
        "ref": getattr(block, "ref", None),
        "label": getattr(block, "label", None),
        "content_type": getattr(block, "content_type", None),
        "content": getattr(block, "content", None),
    }
