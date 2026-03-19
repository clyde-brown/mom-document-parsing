"""재구성 1: 여러 테이블이 하나의 세그먼트에 모여있을 때, 테이블을 자르지 않고 통째로 한 세그먼트로만 재할당."""

from document_parsing_engine.domain.presets.segment_definitions import (
    get_segment_definition,
)
from document_parsing_engine.domain.segment.keyword_bundle import (
    build_segment_keyword_bundle,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
    SegmentBucket,
    BlockSegmentRecommendation,
)
from document_parsing_engine.app.services.document_layout_parsing_service import (
    BlockContent,
)

from document_parsing_engine.domain.segment_reconstruction.segments import (
    segments_without_buckets,
)
from document_parsing_engine.domain.segment_reconstruction.row_scoring import (
    row_scores_with_bonuses,
)


def _assign_table_to_single_segment(
    rows: list,
    keyword_bundle: dict,
    allowed_segments: list[str],
    missing_segments: list[str],
) -> str:
    """테이블 전체 행의 점수를 합산해 한 개의 세그먼트만 반환 (테이블 자르지 않음)."""
    table_scores = {s: 0.0 for s in allowed_segments}
    for row in rows:
        row_scores = row_scores_with_bonuses(row, keyword_bundle, allowed_segments)
        for seg_name in allowed_segments:
            table_scores[seg_name] += row_scores.get(seg_name, 0.0)
    return max(allowed_segments, key=lambda s: table_scores.get(s, 0.0))


def decompose_tables_by_missing_segments(seg, blocks: list):
    """missing 세그먼트가 있을 때 테이블을 자르지 않고 통째로 한 세그먼트로만 재할당. Returns (refined_seg, blocks)."""
    missing = segments_without_buckets(seg)
    if not missing:
        return seg, blocks
    doc_type = getattr(seg, "doc_type", None) or "quotation"
    definition = get_segment_definition(doc_type)
    keyword_bundle = build_segment_keyword_bundle(definition)
    allowed_segments = list(seg.allowed_segments)
    ref_to_primary = {r.block_ref: r.primary_segment for r in seg.block_recommendations}
    ref_to_segment: dict[str, str | None] = {}
    for block in blocks:
        ref = getattr(block, "ref", None)
        if not ref:
            continue
        if getattr(block, "content_type", "") != "table":
            ref_to_segment[ref] = ref_to_primary.get(ref)
            continue
        content = getattr(block, "content", None)
        if not isinstance(content, list) or not content:
            ref_to_segment[ref] = ref_to_primary.get(ref)
            continue
        ref_to_segment[ref] = _assign_table_to_single_segment(
            content, keyword_bundle, allowed_segments, missing
        )
    bucket_refs = {s: [] for s in allowed_segments}
    for r, seg_name in ref_to_segment.items():
        if seg_name and seg_name in bucket_refs:
            bucket_refs[seg_name].append(r)
    segment_buckets = [
        SegmentBucket(segment_name=name, block_refs=refs, reasons=[])
        for name in allowed_segments
        for refs in [bucket_refs[name]]
        if refs
    ]
    block_recommendations = [
        BlockSegmentRecommendation(
            block_ref=getattr(b, "ref", ""),
            label=getattr(b, "label", None),
            content_type=getattr(b, "content_type", ""),
            primary_segment=ref_to_segment.get(getattr(b, "ref", None)),
            candidates=[],
        )
        for b in blocks
        if getattr(b, "ref", None)
    ]
    unmapped = [r for r in ref_to_segment if ref_to_segment.get(r) is None]
    return (
        LayoutSegmentMappingRecommendation(
            doc_type=seg.doc_type,
            allowed_segments=seg.allowed_segments,
            block_recommendations=block_recommendations,
            segment_buckets=segment_buckets,
            unmapped_block_refs=unmapped,
            warnings=seg.warnings,
        ),
        blocks,
    )
