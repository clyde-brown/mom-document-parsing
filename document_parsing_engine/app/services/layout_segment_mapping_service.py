"""
블록→세그먼트 매핑 서비스 (오케스트레이션만).
로직은 domain/segment로 위임.
"""

from __future__ import annotations

from typing import Any

from document_parsing_engine.app.services.document_layout_parsing_service import (
    BlockContent,
)
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
                    ("" if k is None else str(k).strip()): (
                        "" if v is None else str(v).strip()
                    )
                    for k, v in content.items()
                }
            elif isinstance(content, list):
                content = [
                    (
                        ["" if c is None else str(c).strip() for c in row]
                        if isinstance(row, list)
                        else ("" if row is None else str(row).strip())
                    )
                    for row in content
                ]
            normalized.append(
                BlockContent(
                    ref=block.ref.strip(),
                    label=(
                        block.label.strip()
                        if isinstance(block.label, str)
                        else block.label
                    ),
                    content_type=block.content_type.strip(),
                    content=content,
                )
            )
        return normalized

    @staticmethod
    def _seg_str(x: Any) -> str | None:
        if x is None:
            return None
        return x.value if hasattr(x, "value") else str(x)

    @staticmethod
    def _print_block_content(blk: BlockContent | None) -> None:
        """content_type에 따라 블록 내용 출력: text는 그대로, group_kv는 dict 한 줄씩, table은 전부."""
        if blk is None or getattr(blk, "content", None) is None:
            print("      (내용 없음)")
            return
        ct = getattr(blk, "content_type", "")
        content = blk.content
        if ct == "text":
            print(f"      {content}")
        elif ct == "group_kv" and isinstance(content, dict):
            for k, v in content.items():
                print(f"      {k}: {v}")
        elif ct == "table" and isinstance(content, list):
            for row in content:
                if isinstance(row, list):
                    print("      ", row)
                else:
                    print("      ", row)
        else:
            print(f"      {content}")

    def pretty_print(
        self,
        result: LayoutSegmentMappingRecommendation,
        blocks: list[BlockContent],
    ) -> None:
        """세그먼트별로 출력(segment_buckets 기준) + block별 실제 텍스트."""
        blocks_by_ref = {
            getattr(b, "ref", None): b for b in blocks if getattr(b, "ref", None)
        }
        for bucket in result.segment_buckets:
            seg = getattr(bucket, "segment_type", None) or getattr(
                bucket, "segment_name", None
            )
            seg_str = self._seg_str(seg)
            print(f"=== segment: {seg_str} ===")
            print(f"  block_refs: {bucket.block_refs}")
            if bucket.reasons:
                print(
                    f"  reasons: {bucket.reasons[:3]}{'...' if len(bucket.reasons) > 3 else ''}"
                )
            for r in result.block_recommendations:
                r_primary = getattr(r, "primary_segment", None)
                if self._seg_str(r_primary) == seg_str:
                    print(
                        f"    - {r.block_ref} | label={r.label} | content_type={r.content_type}"
                    )
                    self._print_block_content(blocks_by_ref.get(r.block_ref))
            print()

        if result.unmapped_block_refs:
            print("=== unmapped (미매핑) ===")
            print(f"  block_refs: {result.unmapped_block_refs}")
            for ref in result.unmapped_block_refs:
                blk = blocks_by_ref.get(ref)
                if blk:
                    print(f"    - {ref}:")
                    self._print_block_content(blk)
