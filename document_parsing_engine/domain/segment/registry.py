"""정의 기반 규칙 레지스트리: keyword_provider 주입."""

from typing import TYPE_CHECKING, Any

from document_parsing_engine.domain.segment.rules import (
    DefinitionKeywordScoringRule,
    PageFooterIgnoreRule,
    PictureIgnoreRule,
)

if TYPE_CHECKING:
    from document_parsing_engine.domain.segment.base import BlockSegmentRule


class SegmentRuleRegistry:
    def __init__(self, segment_keyword_provider: Any) -> None:
        self._segment_keyword_provider = segment_keyword_provider

    def get_rules(self, doc_type: str) -> list["BlockSegmentRule"]:
        return [
            PageFooterIgnoreRule(),
            PictureIgnoreRule(),
            DefinitionKeywordScoringRule(
                segment_keyword_provider=self._segment_keyword_provider,
            ),
        ]
