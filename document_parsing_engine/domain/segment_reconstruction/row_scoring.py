"""공통 유틸: 행 텍스트 정규화, 키워드 매칭, 행별 세그먼트 점수·보너스."""

from collections import Counter


def normalize_text(text: str) -> str:
    """공백 정규화·소문자화."""
    return " ".join((text or "").strip().lower().split())


def contains_keyword(text: str, keyword: str) -> bool:
    """정규화된 text에 정규화된 keyword가 포함되면 True."""
    return normalize_text(keyword) in normalize_text(text)


def row_text(row: list) -> str:
    """행의 비공란 셀을 공백으로 이어붙인 문자열."""
    parts = []
    for c in row:
        s = ("" if c is None else str(c)).strip()
        if s:
            parts.append(s)
    return " ".join(parts)


def is_row_anchor(row: list) -> str | None:
    """행의 비어있지 않은 셀이 모두 같은 단어이면 그 단어 반환."""
    non_empty = [
        normalize_text(str(c)) for c in row if c is not None and str(c).strip()
    ]
    if not non_empty:
        return None
    first = non_empty[0]
    if all(c == first for c in non_empty):
        return first
    return None


def score_row_by_keywords(
    row: list, keyword_bundle: dict, allowed_segments: list[str]
) -> dict[str, float]:
    """한 행의 셀 텍스트로 세그먼트별 키워드 매칭 점수 (필드 + 세그먼트 키워드)."""
    text = row_text(row)
    scores = {s: 0.0 for s in allowed_segments}
    for seg_name in allowed_segments:
        bundle = keyword_bundle.get(seg_name, {})
        for keyword, boost in bundle.get("field_keywords", []) + bundle.get(
            "segment_keywords", []
        ):
            if contains_keyword(text, keyword):
                scores[seg_name] += boost
    return scores


def even_cell_quotation_meta_bonus(row: list, keyword_bundle: dict) -> float:
    """짝수 셀 + 짝수 열(0,2,4,...)에 quotation_meta 키워드 매칭 시에만 0.15."""
    n = len([c for c in row if c is not None and str(c).strip()])
    if n < 2 or n % 2 != 0:
        return 0.0
    even_col_parts = [
        str(row[i]).strip()
        for i in range(0, len(row), 2)
        if i < len(row) and row[i] is not None and str(row[i]).strip()
    ]
    even_col_text = " ".join(even_col_parts)
    if not even_col_text:
        return 0.0
    bundle = keyword_bundle.get("quotation_meta", {})
    keywords = [
        kw
        for kw, _ in bundle.get("field_keywords", [])
        + bundle.get("segment_keywords", [])
    ]
    for kw in keywords:
        if contains_keyword(even_col_text, kw):
            return 0.15
    return 0.0


def repeated_word_remarks_bonus(row: list) -> float:
    """한 행에서 같은 단어가 70% 이상이면 remarks 보너스 0.05."""
    non_empty = [str(c).strip() for c in row if c is not None and str(c).strip()]
    if not non_empty:
        return 0.0
    most_common_count = Counter(non_empty).most_common(1)[0][1]
    return 0.05 if most_common_count / len(non_empty) >= 0.7 else 0.0


def row_scores_with_bonuses(
    row: list, keyword_bundle: dict, allowed_segments: list[str]
) -> dict[str, float]:
    """키워드 점수 + quotation_meta 짝수열 보너스 + remarks 반복어 보너스."""
    scores = score_row_by_keywords(row, keyword_bundle, allowed_segments)
    if "quotation_meta" in allowed_segments:
        scores["quotation_meta"] = scores.get(
            "quotation_meta", 0.0
        ) + even_cell_quotation_meta_bonus(row, keyword_bundle)
    if "remarks" in allowed_segments:
        scores["remarks"] = scores.get("remarks", 0.0) + repeated_word_remarks_bonus(
            row
        )
    return scores
