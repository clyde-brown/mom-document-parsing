"""재구성 2.2: 헤더 run 기준 열 병합, 셀 내 단어 중복 제거, remarks 키워드가 걸리는 열만 remarks로 분리."""

import re

from document_parsing_engine.domain.presets.segment_definitions import (
    get_segment_definition,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
    SegmentBucket,
    BlockSegmentRecommendation,
)
from document_parsing_engine.app.services.document_layout_parsing_service import (
    BlockContent,
)


def _remarks_column_indices(first_row: list, remarks_keywords: tuple) -> set[int]:
    """헤더(first_row) 셀 중 remarks 키워드가 포함된 열 인덱스 집합."""
    indices = set()
    for j, cell in enumerate(first_row):
        cell_text = ("" if cell is None else str(cell)).strip()
        if any(kw in cell_text for kw in remarks_keywords):
            indices.add(j)
    return indices


def _clean_section_cell(cell) -> str:
    """셀에서 앞쪽 '숫자.' 또는 '숫자. ' 제거 후 반환."""
    if cell is None:
        return ""
    s = str(cell).strip()
    return re.sub(r"^\d+\.\s*", "", s).strip()


def _runs_of_same(cleaned: list[str]) -> list[tuple[str, int]]:
    """연속된 같은(비공란) 값만 (값, 연속 개수) 리스트로."""
    runs = []
    for c in cleaned:
        if not c:
            continue
        if runs and runs[-1][0] == c:
            runs[-1] = (c, runs[-1][1] + 1)
        else:
            runs.append((c, 1))
    return runs


def get_run_lengths_from_header_row(header_row: list) -> list[int]:
    """
    헤더 행에서 run(연속 같은 값) 길이 목록을 반환.
    빈 셀은 뒷열(다음 비공란 열)과 합쳐서 한 run으로 묶고, 맨 뒤 빈 셀들은 직전 run에 흡수.
    반환 길이 합은 len(header_row).
    """
    cleaned = [_clean_section_cell(c) for c in header_row]
    run_lengths = []
    i = 0
    n = len(cleaned)
    pending_empty = 0
    while i < n:
        c = cleaned[i]
        if not c:
            pending_empty += 1
            i += 1
            continue
        run_len = pending_empty + 1
        pending_empty = 0
        i += 1
        while i < n and cleaned[i] == c:
            run_len += 1
            i += 1
        run_lengths.append(run_len)
    if pending_empty and run_lengths:
        run_lengths[-1] += pending_empty
    elif pending_empty:
        run_lengths.append(pending_empty)
    return run_lengths


def merge_data_row_by_runs(row: list, run_lengths: list[int]) -> list[str]:
    """
    데이터 행을 run 구간별로 잘라, 각 구간의 셀을 한 문자열로 합쳐서 반환.
    """
    out = []
    start = 0
    for length in run_lengths:
        end = start + length
        chunk = row[start:end] if end <= len(row) else row[start:]
        merged = " ".join(str(c).strip() for c in chunk if str(c).strip())
        out.append(merged)
        start = end
    return out


def _dedupe_words_in_cell(text: str) -> str:
    """띄어쓰기 기준으로 단어를 나누어, 같은 단어 중복 제거(첫 등장만 유지)."""
    if text is None:
        return ""
    s = str(text).strip()
    if not s:
        return ""
    seen = set()
    words = s.split()
    return " ".join(w for w in words if w not in seen and not seen.add(w))


def normalize_and_merge_section_row(row: list, cells_per_run: int = 2) -> list[str]:
    """
    각 셀에서 앞 '숫자.' 제거. 연속된 같은 값은 한 run으로 보고, run당 cells_per_run개 셀로 내보냄.
    """
    cleaned = [_clean_section_cell(c) for c in row]
    runs = _runs_of_same(cleaned)
    out = []
    for value, _ in runs:
        for _ in range(cells_per_run):
            out.append(value)
    return out


def merge_table_content_by_header_runs(content: list) -> list:
    """테이블 content(행 리스트)에 대해 첫 행을 헤더로 run 병합, 나머지 데이터 행은 run별 한 칸으로 합쳐 반환."""
    if not content:
        return []
    header_row = content[0]
    run_lengths = get_run_lengths_from_header_row(header_row)
    # 헤더도 run_lengths 기준으로 run당 1칸
    header_merged = []
    start = 0
    for length in run_lengths:
        chunk = header_row[start : start + length]
        val = next(
            (_clean_section_cell(c) for c in chunk if _clean_section_cell(c)), ""
        )
        header_merged.append(val)
        start += length
    merged_rows = [header_merged]
    for row in content[1:]:
        merged_rows.append(merge_data_row_by_runs(row, run_lengths))
    merged_rows = [[_dedupe_words_in_cell(c) for c in row] for row in merged_rows]
    return merged_rows


def apply_column_merge_and_remarks(seg, blocks: list):
    """
    테이블 블록에 헤더 run 기준 열 병합 + 단어 중복 제거 적용 후,
    헤더에 remarks 키워드가 걸리는 열만 별도 블록으로 분리해 remarks 세그먼트로 보냄.
    Returns (refined_seg, refined_blocks).
    """
    definition = get_segment_definition(getattr(seg, "doc_type", None) or "quotation")
    remarks_keywords = ()
    for s in definition.segments:
        if getattr(s, "name", None) == "remarks":
            remarks_keywords = tuple(s.metadata.get("segment_keywords", ()))
            break

    ref_to_segment = {r.block_ref: r.primary_segment for r in seg.block_recommendations}
    merged_blocks = []

    for block in blocks:
        ref = getattr(block, "ref", None)
        content_type = getattr(block, "content_type", "")
        content = getattr(block, "content", None)
        label = getattr(block, "label", "table")

        if content_type != "table" or not isinstance(content, list) or len(content) < 1:
            merged_blocks.append(block)
            continue

        merged_content = merge_table_content_by_header_runs(content)
        first_row = merged_content[0]
        remarks_cols = _remarks_column_indices(first_row, remarks_keywords)
        n_cols = len(first_row)

        if not remarks_cols:
            merged_blocks.append(
                BlockContent(
                    ref=ref, label=label, content_type="table", content=merged_content
                )
            )
            continue

        if remarks_cols == set(range(n_cols)):
            merged_blocks.append(
                BlockContent(
                    ref=ref, label=label, content_type="table", content=merged_content
                )
            )
            ref_to_segment[ref] = "remarks"
            continue

        non_remarks_cols = [j for j in range(n_cols) if j not in remarks_cols]
        remarks_col_list = sorted(remarks_cols)
        content_main = [[row[j] for j in non_remarks_cols] for row in merged_content]
        content_remarks = [[row[j] for j in remarks_col_list] for row in merged_content]

        merged_blocks.append(
            BlockContent(
                ref=ref, label=label, content_type="table", content=content_main
            )
        )
        ref_remarks = f"{ref}@remarks"
        merged_blocks.append(
            BlockContent(
                ref=ref_remarks,
                label=label,
                content_type="table",
                content=content_remarks,
            )
        )
        ref_to_segment[ref_remarks] = "remarks"

    allowed_segments = list(seg.allowed_segments)
    if (
        any(ref_to_segment.get(r) == "remarks" for r in ref_to_segment)
        and "remarks" not in allowed_segments
    ):
        allowed_segments.append("remarks")
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
        for b in merged_blocks
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
    return refined_seg, merged_blocks
