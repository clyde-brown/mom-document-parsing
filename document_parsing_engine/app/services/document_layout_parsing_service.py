"""
문서 레이아웃 파싱: 블록 목록 추출, 그룹 KV 파싱, 테이블 행 추출.
Docling Parser에 의존 (doc_dict는 Docling export_to_dict() 형식).
"""

from dataclasses import dataclass
from typing import Any

from document_parsing_engine.domain.layout.doc_blocks import (
    get_blocks_sorted,
    get_group_texts_in_order,
)
from document_parsing_engine.domain.models.section import Section
from document_parsing_engine.domain.parsers.section.group_kv_section_parser import (
    GroupKVSectionParser,
)
from document_parsing_engine.domain.parsers.table_parser import get_table_rows


@dataclass
class BlockContent:
    """단일 블록 파싱 결과."""
    ref: str
    label: str
    content_type: str  # "text" | "group_kv" | "table" | "picture"
    content: Any  # str | dict[str, str] | list[list[str]] | None


class DocumentLayoutParsingService:
    """Docling export doc_dict에 대해 블록 순서 추출 및 그룹/테이블 파싱."""

    def __init__(
        self,
        y_tol: float = 10.0,
        min_gap_threshold: float = 18.0,
        gap_ratio: float = 1.8,
    ):
        self._group_parser = GroupKVSectionParser(
            y_tol=y_tol,
            min_gap_threshold=min_gap_threshold,
            gap_ratio=gap_ratio,
        )

    def get_blocks_sorted(self, doc_dict: dict) -> list[tuple[str, dict]]:
        """문서 내 블록을 문서 순서대로 (ref, obj) 리스트로 반환."""
        return get_blocks_sorted(doc_dict)

    def parse_layout(
        self,
        doc_dict: dict,
        group_known_keys_map: dict[str, set[str]] | None = None,
    ) -> list[BlockContent]:
        """블록 추출 + 파싱을 한 번에 수행해 BlockContent 리스트만 반환."""
        blocks_sorted = self.get_blocks_sorted(doc_dict)
        return self.parse_blocks(
            doc_dict,
            group_known_keys_map=group_known_keys_map or {},
            blocks_sorted=blocks_sorted,
        )

    def parse_group_kv(
        self,
        doc_dict: dict,
        group_ref: str,
        known_keys: set[str] | None = None,
    ) -> dict[str, str]:
        """그룹 하나를 key-value dict로 파싱. known_keys는 GroupKVSectionParser에 전달."""
        from document_parsing_engine.utils.refs import resolve_ref
        group_obj = resolve_ref(doc_dict, group_ref)
        section = Section(
            ref=group_ref,
            label=group_obj.get("label", ""),
            kind="group_kv",
            raw_obj=group_obj,
        )
        if known_keys is not None:
            parser = GroupKVSectionParser(
                y_tol=10.0,
                min_gap_threshold=18.0,
                gap_ratio=1.8,
                known_keys=known_keys,
            )
        else:
            parser = self._group_parser
        return parser.parse(doc_dict, section)

    def get_table_rows(self, table_obj: dict) -> list[list[str]]:
        """테이블 블록에서 행별 셀 텍스트 리스트 반환."""
        return get_table_rows(table_obj)

    def get_group_texts_in_order(self, doc_dict: dict, group_obj: dict) -> list[str]:
        """그룹 children을 좌표 순으로 정렬한 텍스트 리스트 (폴백/출력용)."""
        return get_group_texts_in_order(doc_dict, group_obj)

    def parse_blocks(
        self,
        doc_dict: dict,
        group_known_keys_map: dict[str, set[str]] | None = None,
        blocks_sorted: list[tuple[str, dict]] | None = None,
    ) -> list[BlockContent]:
        """
        전체 블록을 파싱해 BlockContent 리스트 반환.
        blocks_sorted를 주지 않으면 get_blocks_sorted(doc_dict)로 계산.
        """
        if blocks_sorted is None:
            blocks_sorted = self.get_blocks_sorted(doc_dict)
        group_known_keys_map = group_known_keys_map or {}
        result: list[BlockContent] = []

        for ref, obj in blocks_sorted:
            label = obj.get("label", "")
            self_ref = obj.get("self_ref", "")
            name = obj.get("name", "")

            # text
            if "text" in obj and obj.get("text"):
                result.append(BlockContent(
                    ref=ref,
                    label=label,
                    content_type="text",
                    content=obj["text"],
                ))
                continue

            # group -> group_kv 파싱 시도, 실패 시 텍스트 리스트
            if self_ref.startswith("#/groups/") or name == "group":
                known_keys = group_known_keys_map.get(ref)
                try:
                    parsed = self.parse_group_kv(doc_dict, ref, known_keys=known_keys)
                    if parsed:
                        result.append(BlockContent(
                            ref=ref,
                            label=label,
                            content_type="group_kv",
                            content=parsed,
                        ))
                    else:
                        texts = self.get_group_texts_in_order(doc_dict, obj)
                        result.append(BlockContent(
                            ref=ref,
                            label=label,
                            content_type="group_kv",
                            content={"_fallback_texts": texts},
                        ))
                except Exception:
                    texts = self.get_group_texts_in_order(doc_dict, obj)
                    result.append(BlockContent(
                        ref=ref,
                        label=label,
                        content_type="group_kv",
                        content={"_fallback_texts": texts},
                    ))
                continue

            # table
            if self_ref.startswith("#/tables/"):
                rows = self.get_table_rows(obj)
                result.append(BlockContent(
                    ref=ref,
                    label=label,
                    content_type="table",
                    content=rows,
                ))
                continue

            # picture
            if self_ref.startswith("#/pictures/") or label == "picture":
                result.append(BlockContent(
                    ref=ref,
                    label=label,
                    content_type="picture",
                    content=None,
                ))
                continue

            result.append(BlockContent(
                ref=ref,
                label=label,
                content_type="unknown",
                content=None,
            ))

        return result

    def print_blocks_content(
        self,
        doc_dict: dict,
        group_known_keys_map: dict[str, set[str]] | None = None,
        blocks_sorted: list[tuple[str, dict]] | None = None,
    ) -> None:
        """parse_blocks 결과를 노트북 스타일로 출력 (호환용)."""
        blocks = self.parse_blocks(
            doc_dict,
            group_known_keys_map=group_known_keys_map,
            blocks_sorted=blocks_sorted,
        )
        for i, blk in enumerate(blocks):
            print(f"\n[{i}] {blk.ref}  label={blk.label}")
            if blk.content_type == "text":
                print(blk.content)
            elif blk.content_type == "group_kv":
                if isinstance(blk.content, dict):
                    if "_fallback_texts" in blk.content:
                        for t in blk.content["_fallback_texts"]:
                            print(f"    - {t}")
                    else:
                        for k, v in blk.content.items():
                            print(f"    - {k}: {v}")
            elif blk.content_type == "table":
                for row_idx, row in enumerate(blk.content or []):
                    print(f"    row[{row_idx}] = {row}")
            elif blk.content_type == "picture":
                print("    [PICTURE]")
            else:
                print("    [NO RENDERABLE CONTENT]")
