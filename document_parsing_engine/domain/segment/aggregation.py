"""블록 추천 결과 집계: merge, primary 선택, buckets, warnings."""

from document_parsing_engine.domain.models.segment_mapping_result import (
    BlockSegmentRecommendation,
    SegmentBucket,
    SegmentCandidate,
)


def dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for v in values:
        if v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def merge_candidates(
    candidates: list[SegmentCandidate],
) -> list[SegmentCandidate]:
    """동일 segment_name 후보 병합: max score, reasons 합침, dedupe 후 점수 내림차순."""
    merged: dict[str, SegmentCandidate] = {}
    for c in candidates:
        existing = merged.get(c.segment_name)
        if existing is None:
            merged[c.segment_name] = SegmentCandidate(
                segment_name=c.segment_name,
                score=c.score,
                reasons=list(c.reasons),
            )
            continue
        existing.score = max(existing.score, c.score)
        existing.reasons.extend(c.reasons)
    result = list(merged.values())
    for item in result:
        item.reasons = dedupe_keep_order(item.reasons)
    result.sort(key=lambda x: x.score, reverse=True)
    return result


def select_primary_segment(
    candidates: list[SegmentCandidate],
    threshold: float,
) -> str | None:
    if not candidates:
        return None
    best = candidates[0]
    if best.score < threshold:
        return None
    return best.segment_name


def build_segment_buckets(
    allowed_segments: tuple[str, ...],
    block_recommendations: list[BlockSegmentRecommendation],
) -> list[SegmentBucket]:
    buckets = {name: SegmentBucket(segment_name=name) for name in allowed_segments}
    for rec in block_recommendations:
        if rec.primary_segment is None:
            continue
        bucket = buckets[rec.primary_segment]
        bucket.block_refs.append(rec.block_ref)
        if rec.candidates:
            top = next(
                (c for c in rec.candidates if c.segment_name == rec.primary_segment),
                rec.candidates[0],
            )
            bucket.reasons.extend(top.reasons)
    result = []
    for name in allowed_segments:
        b = buckets[name]
        if not b.block_refs:
            continue
        b.reasons = dedupe_keep_order(b.reasons)
        result.append(b)
    return result


def build_warnings(
    allowed_segments: tuple[str, ...],
    block_recommendations: list[BlockSegmentRecommendation],
    unmapped_block_refs: list[str],
) -> list[str]:
    warnings: list[str] = []
    found = {r.primary_segment for r in block_recommendations if r.primary_segment is not None}
    for name in allowed_segments:
        if name not in found:
            warnings.append(f"{name} segment not found")
    if unmapped_block_refs:
        warnings.append(f"{len(unmapped_block_refs)} block(s) are unmapped")
    return warnings
