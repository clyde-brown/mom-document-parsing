"""정의 기반 블록→세그먼트 매핑 추천 결과 (segment_name: str)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SegmentCandidate:
    segment_name: str
    score: float
    reasons: list[str] = field(default_factory=list)


@dataclass
class BlockSegmentRecommendation:
    block_ref: str
    label: str | None
    content_type: str
    primary_segment: str | None
    candidates: list[SegmentCandidate] = field(default_factory=list)


@dataclass
class SegmentBucket:
    segment_name: str
    block_refs: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


@dataclass
class LayoutSegmentMappingRecommendation:
    doc_type: str
    allowed_segments: list[str]
    block_recommendations: list[BlockSegmentRecommendation] = field(default_factory=list)
    segment_buckets: list[SegmentBucket] = field(default_factory=list)
    unmapped_block_refs: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
