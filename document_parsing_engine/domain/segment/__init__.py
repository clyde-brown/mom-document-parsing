"""세그먼트: 정의 소스/Provider, 규칙, 키워드 번들, 집계, 블록 추천."""

from document_parsing_engine.domain.segment.aggregation import (
    build_segment_buckets,
    build_warnings,
    merge_candidates,
    select_primary_segment,
)
from document_parsing_engine.domain.segment.base import (
    BaseBlockSegmentRule,
    BlockSegmentRule,
)
from document_parsing_engine.domain.segment.keyword_bundle import (
    build_segment_keyword_bundle,
)
from document_parsing_engine.domain.segment.mapping import recommend_for_block
from document_parsing_engine.domain.segment.registry import SegmentRuleRegistry
from document_parsing_engine.domain.segment.rules import (
    DefinitionKeywordScoringRule,
    PageFooterIgnoreRule,
    PictureIgnoreRule,
)
from document_parsing_engine.domain.segment.source import (
    InMemorySegmentDefinitionSource,
    SegmentDefinitionProvider,
)

__all__ = [
    "BaseBlockSegmentRule",
    "BlockSegmentRule",
    "build_segment_buckets",
    "build_segment_keyword_bundle",
    "build_warnings",
    "DefinitionKeywordScoringRule",
    "InMemorySegmentDefinitionSource",
    "merge_candidates",
    "PageFooterIgnoreRule",
    "PictureIgnoreRule",
    "recommend_for_block",
    "SegmentDefinitionProvider",
    "SegmentRuleRegistry",
    "select_primary_segment",
]
