"""정의 기반 규칙: DefinitionKeywordScoringRule, Ignore 규칙."""

from typing import Any

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
    SegmentDefinition,
)
from document_parsing_engine.domain.models.segment_mapping_result import SegmentCandidate

from document_parsing_engine.domain.segment.base import BaseBlockSegmentRule


class PictureIgnoreRule(BaseBlockSegmentRule):
    def supports(
        self,
        *,
        doc_type: str,
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> bool:
        return getattr(block, "content_type", "") == "picture"

    def score(
        self,
        *,
        doc_type: str,
        doc_dict: dict[str, Any],
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> list[SegmentCandidate]:
        return []


class PageFooterIgnoreRule(BaseBlockSegmentRule):
    def supports(
        self,
        *,
        doc_type: str,
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> bool:
        return getattr(block, "label", None) == "page_footer"

    def score(
        self,
        *,
        doc_type: str,
        doc_dict: dict[str, Any],
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> list[SegmentCandidate]:
        return []


class DefinitionKeywordScoringRule(BaseBlockSegmentRule):
    def __init__(self, segment_keyword_provider: Any) -> None:
        self._segment_keyword_provider = segment_keyword_provider

    def supports(
        self,
        *,
        doc_type: str,
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> bool:
        return getattr(block, "content_type", "") in {"text", "group_kv", "table"}

    def score(
        self,
        *,
        doc_type: str,
        doc_dict: dict[str, Any],
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> list[SegmentCandidate]:
        text = self._text_of(block)
        if not text:
            return []

        segment_keyword_map = self._segment_keyword_provider(document_definition)
        candidates: list[SegmentCandidate] = []

        for segment in document_definition.segments:
            score = self._base_score_for_block(block=block, segment=segment)
            reasons: list[str] = []
            matched_keywords: list[str] = []

            keyword_bundle = segment_keyword_map.get(segment.name, {})

            for keyword, boost_score in keyword_bundle.get("field_keywords", []):
                if self._contains_keyword(text, keyword):
                    score += boost_score
                    matched_keywords.append(keyword)
            if matched_keywords:
                score += min(len(matched_keywords) * 0.015, 0.12)
                reasons.append(f"field keywords matched: {', '.join(matched_keywords[:10])}")

            segment_matches: list[str] = []
            for keyword, boost_score in keyword_bundle.get("segment_keywords", []):
                if self._contains_keyword(text, keyword):
                    score += boost_score
                    segment_matches.append(keyword)
            if segment_matches:
                reasons.append(f"segment keywords matched: {', '.join(segment_matches[:8])}")

            if getattr(block, "label", None) == "section_header":
                title_matches: list[str] = []
                for keyword, boost_score in keyword_bundle.get("title_keywords", []):
                    if self._contains_keyword(text, keyword):
                        score += boost_score
                        title_matches.append(keyword)
                if title_matches:
                    reasons.append(f"title keywords matched: {', '.join(title_matches[:8])}")

            if not reasons:
                continue

            reasons.append(f"content_type={getattr(block, 'content_type', '')}")
            if getattr(block, "label", None):
                reasons.append(f"label={block.label}")

            candidates.append(self._candidate(segment.name, score, *reasons))

        return candidates

    @staticmethod
    def _base_score_for_block(
        *,
        block: Any,
        segment: SegmentDefinition,
    ) -> float:
        score = 0.12
        preferred_block_types = tuple(segment.metadata.get("preferred_block_types", ()))
        preferred_labels = tuple(segment.metadata.get("preferred_labels", ()))
        content_type = getattr(block, "content_type", "")
        label = getattr(block, "label", None)

        if content_type in preferred_block_types:
            score += 0.18
        if label and label in preferred_labels:
            score += 0.08
        if content_type == "table" and segment.name == "items":
            score += 0.20
        if content_type == "group_kv" and segment.name.endswith("meta"):
            score += 0.12
        if label == "list" and segment.name == "remarks":
            score += 0.10
        return score
