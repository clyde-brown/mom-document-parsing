"""
세그먼트 재구성 서비스 (얇은 오케스트레이션).
분기 및 도메인 호출만 담당. 핵심 로직은 domain/segment_reconstruction에 위임.
"""

from __future__ import annotations

from document_parsing_engine.app.services.document_layout_parsing_service import (
    BlockContent,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
)
from document_parsing_engine.domain.segment_reconstruction import (
    segments_without_buckets,
    has_multiple_tables_in_any_bucket,
    decompose_tables_by_missing_segments,
    decompose_merged_tables_by_row_sections,
    apply_column_merge_and_remarks,
)


def reconstruct(
    seg: LayoutSegmentMappingRecommendation,
    blocks: list[BlockContent],
) -> tuple[LayoutSegmentMappingRecommendation, list[BlockContent]]:
    """
    Input: seg, blocks.
    Output: refined_seg, refined_blocks.

    - 버킷이 없는 세그먼트가 없으면 seg, blocks 그대로 반환.
    - 다수의 테이블이 하나의 세그먼트에 모여 있으면 재구성 1 (decompose_tables_by_missing_segments).
    - 테이블 하나만 존재하면 재구성 2.1 행분해 후 2.2 열분해 + remarks 이동.
    """
    missing = segments_without_buckets(seg)
    if not missing:
        return seg, blocks

    if has_multiple_tables_in_any_bucket(seg, blocks):
        return decompose_tables_by_missing_segments(seg, blocks)

    refined_seg, refined_blocks = decompose_merged_tables_by_row_sections(seg, blocks)
    return apply_column_merge_and_remarks(refined_seg, refined_blocks)


class SegmentReconstructionService:
    """세그먼트 재구성 서비스. reconstruct(seg, blocks) -> (refined_seg, refined_blocks)."""

    def reconstruct(
        self,
        seg: LayoutSegmentMappingRecommendation,
        blocks: list[BlockContent],
    ) -> tuple[LayoutSegmentMappingRecommendation, list[BlockContent]]:
        return reconstruct(seg, blocks)
