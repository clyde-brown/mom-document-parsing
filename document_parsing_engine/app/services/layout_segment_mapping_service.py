"""
블록→세그먼트 매핑 서비스 (오케스트레이션만).
로직은 domain/segment로 위임.
"""

from __future__ import annotations

from typing import Any

from document_parsing_engine.app.services.document_layout_parsing_service import BlockContent
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
)
from document_parsing_engine.domain.segment import (
    build_segment_buckets,
    build_segment_keyword_bundle,
    build_warnings,
    recommend_for_block,
    SegmentDefinitionProvider,
    SegmentRuleRegistry,
)


class LayoutSegmentMappingService:
    def __init__(
        self,
        rule_registry: SegmentRuleRegistry | None = None,
        definition_provider: SegmentDefinitionProvider | None = None,
        primary_threshold: float = 0.50,
    ) -> None:
        self._definition_provider = definition_provider or SegmentDefinitionProvider()
        self._rule_registry = rule_registry or SegmentRuleRegistry(
            segment_keyword_provider=build_segment_keyword_bundle,
        )
        self._primary_threshold = primary_threshold

    def recommend(
        self,
        *,
        doc_type: str,
        doc_dict: dict[str, Any],
        blocks: list[BlockContent],
    ) -> LayoutSegmentMappingRecommendation:
        document_definition = self._definition_provider.get(doc_type)
        allowed_segments = tuple(s.name for s in document_definition.segments)
        normalized_blocks = self._normalize_blocks(blocks)
        rules = self._rule_registry.get_rules(doc_type)

        block_recommendations = [
            recommend_for_block(
                doc_type=doc_type,
                doc_dict=doc_dict,
                document_definition=document_definition,
                block=block,
                rules=rules,
                primary_threshold=self._primary_threshold,
            )
            for block in normalized_blocks
        ]

        segment_buckets = build_segment_buckets(
            allowed_segments=allowed_segments,
            block_recommendations=block_recommendations,
        )
        unmapped_block_refs = [
            r.block_ref for r in block_recommendations if r.primary_segment is None
        ]
        warnings = build_warnings(
            allowed_segments=allowed_segments,
            block_recommendations=block_recommendations,
            unmapped_block_refs=unmapped_block_refs,
        )

        return LayoutSegmentMappingRecommendation(
            doc_type=document_definition.doc_type,
            allowed_segments=list(allowed_segments),
            block_recommendations=block_recommendations,
            segment_buckets=segment_buckets,
            unmapped_block_refs=unmapped_block_refs,
            warnings=warnings,
        )

    def _normalize_blocks(self, blocks: list[BlockContent]) -> list[BlockContent]:
        """BlockContent 리스트 정규화 (app 전용: BlockContent 타입 유지)."""
        normalized: list[BlockContent] = []
        for block in blocks:
            content = block.content
            if isinstance(content, str):
                content = content.strip()
            elif isinstance(content, dict):
                content = {
                    ("" if k is None else str(k).strip()): ("" if v is None else str(v).strip())
                    for k, v in content.items()
                }
            elif isinstance(content, list):
                content = [
                    ["" if c is None else str(c).strip() for c in row]
                    if isinstance(row, list)
                    else ("" if row is None else str(row).strip())
                    for row in content
                ]
            normalized.append(
                BlockContent(
                    ref=block.ref.strip(),
                    label=block.label.strip() if isinstance(block.label, str) else block.label,
                    content_type=block.content_type.strip(),
                    content=content,
                )
            )
        return normalized
