"""정의 기반 블록→세그먼트 규칙 Protocol 및 Base (block은 Any로 app 의존 제거)."""

from __future__ import annotations

from typing import Any, Protocol

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
)
from document_parsing_engine.domain.models.segment_mapping_result import SegmentCandidate


class BlockSegmentRule(Protocol):
    def supports(
        self,
        *,
        doc_type: str,
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> bool: ...

    def score(
        self,
        *,
        doc_type: str,
        doc_dict: dict[str, Any],
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> list[SegmentCandidate]: ...


class BaseBlockSegmentRule:
    def supports(
        self,
        *,
        doc_type: str,
        document_definition: DocumentSegmentDefinition,
        block: Any,
    ) -> bool:
        return True

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.strip().lower().split())

    @classmethod
    def _text_of(cls, block: Any) -> str:
        if getattr(block, "content", None) is None:
            return ""
        content = block.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, dict):
            parts: list[str] = []
            for k, v in content.items():
                key = "" if k is None else str(k).strip()
                val = "" if v is None else str(v).strip()
                if key:
                    parts.append(key)
                if val:
                    parts.append(val)
            return " ".join(parts).strip()
        if isinstance(content, list):
            parts2: list[str] = []
            for row in content:
                if isinstance(row, list):
                    for cell in row:
                        cell_text = "" if cell is None else str(cell).strip()
                        if cell_text:
                            parts2.append(cell_text)
                else:
                    row_text = "" if row is None else str(row).strip()
                    if row_text:
                        parts2.append(row_text)
            return " ".join(parts2).strip()
        return str(content).strip()

    @classmethod
    def _contains_keyword(cls, text: str, keyword: str) -> bool:
        normalized_text = cls._normalize_text(text)
        normalized_keyword = cls._normalize_text(keyword)
        return normalized_keyword in normalized_text

    @staticmethod
    def _candidate(
        segment_name: str,
        score: float,
        *reasons: str,
    ) -> SegmentCandidate:
        return SegmentCandidate(
            segment_name=segment_name,
            score=max(0.0, min(score, 0.99)),
            reasons=[r for r in reasons if r],
        )
