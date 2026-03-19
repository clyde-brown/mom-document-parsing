"""재구성 2.1: 표가 하나로 합쳐져 있을 때 행 기준으로 items 구간을 잘라 quotation_meta / items에 재할당."""

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
    normalize_text,
    score_row_by_keywords,
)


def _items_score_for_row(row: list, keyword_bundle: dict) -> float:
    """한 행에 대해 items 세그먼트만 점수 (필드+세그먼트 키워드)."""
    scores = score_row_by_keywords(row, keyword_bundle, ["items"])
    return scores.get("items", 0.0)


def _find_items_start_row(rows: list, keyword_bundle: dict) -> int:
    """전체 행을 돌려 items 점수가 최대인 행 인덱스를 반환 (items 구간 시작)."""
    if not rows:
        return 0
    best_idx = 0
    best_score = _items_score_for_row(rows[0], keyword_bundle)
    for i in range(1, len(rows)):
        s = _items_score_for_row(rows[i], keyword_bundle)
        if s > best_score:
            best_score = s
            best_idx = i
    return best_idx


def _non_empty_cell_count(row: list) -> int:
    """공란 제외한 셀 개수."""
    return len([c for c in row if c is not None and str(c).strip()])


def _is_all_same_value_row(row: list) -> bool:
    """공란 제외 후 셀이 2개 이상이고 모두 동일하면 True."""
    non_empty = [
        normalize_text(str(c)) for c in row if c is not None and str(c).strip()
    ]
    if len(non_empty) < 2:
        return False
    return all(c == non_empty[0] for c in non_empty)


def _find_items_end_row(rows: list, start_row: int) -> int:
    """start_row 아래로 내려가며, 열 개수 변경 또는 '모든 열 값 동일' 행 직전까지가 items."""
    n = len(rows)
    if start_row >= n:
        return start_row
    ref_cols = len(rows[start_row])
    end_row = start_row
    for i in range(start_row + 1, n):
        row = rows[i]
        if len(row) != ref_cols:
            return i - 1
        if _is_all_same_value_row(row):
            return i - 1
        end_row = i
    return end_row


def _split_table_rows_into_sections(
    rows: list, keyword_bundle: dict
) -> tuple[list, list]:
    """(quotation_meta_rows, items_rows) 반환."""
    if not rows:
        return [], []
    start = _find_items_start_row(rows, keyword_bundle)
    end = _find_items_end_row(rows, start)
    items_rows = rows[start : end + 1]
    above = rows[:start] if start > 0 else []
    below = rows[end + 1 :] if end + 1 < len(rows) else []
    quotation_meta_rows = above + below
    return quotation_meta_rows, items_rows


def decompose_merged_tables_by_row_sections(seg, blocks: list):
    """테이블이 합쳐져 있을 때 행 기준으로 items 구간을 잘라 quotation_meta / items에 재할당. Returns (refined_seg, refined_blocks)."""
    missing = segments_without_buckets(seg)
    if not missing:
        return seg, blocks
    doc_type = getattr(seg, "doc_type", None) or "quotation"
    definition = get_segment_definition(doc_type)
    keyword_bundle = build_segment_keyword_bundle(definition)
    allowed_segments = list(seg.allowed_segments)
    ref_to_primary = {r.block_ref: r.primary_segment for r in seg.block_recommendations}
    new_blocks = []
    ref_to_segment = {}
    for block in blocks:
        ref = getattr(block, "ref", None)
        content_type = getattr(block, "content_type", "")
        if not ref:
            continue
        if content_type != "table":
            new_blocks.append(block)
            ref_to_segment[ref] = ref_to_primary.get(ref)
            continue
        content = getattr(block, "content", None)
        if not isinstance(content, list) or not content:
            new_blocks.append(block)
            ref_to_segment[ref] = ref_to_primary.get(ref)
            continue
        meta_rows, items_rows = _split_table_rows_into_sections(content, keyword_bundle)
        label = getattr(block, "label", "table")
        if meta_rows:
            ref_meta = f"{ref}@quotation_meta"
            new_blocks.append(
                BlockContent(
                    ref=ref_meta, label=label, content_type="table", content=meta_rows
                )
            )
            ref_to_segment[ref_meta] = "quotation_meta"
        if items_rows:
            ref_items = f"{ref}@items"
            new_blocks.append(
                BlockContent(
                    ref=ref_items, label=label, content_type="table", content=items_rows
                )
            )
            ref_to_segment[ref_items] = "items"
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
        for b in new_blocks
        if getattr(b, "ref", None)
    ]
    unmapped = [r for r in ref_to_segment if ref_to_segment.get(r) is None]
    refined_seg = LayoutSegmentMappingRecommendation(
        doc_type=seg.doc_type,
        allowed_segments=seg.allowed_segments,
        block_recommendations=block_recommendations,
        segment_buckets=segment_buckets,
        unmapped_block_refs=unmapped,
        warnings=seg.warnings,
    )
    return refined_seg, new_blocks
