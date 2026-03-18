"""정의 기반 세그먼트: 필드/세그먼트/문서 정의 모델 및 Source Protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class FieldKeywordDefinition:
    keywords: tuple[str, ...] = field(default_factory=tuple)
    boost_score: float = 0.0


@dataclass(frozen=True)
class FieldDefinition:
    name: str
    description: str | None = None
    required: bool = False
    data_type: str = "string"
    children: tuple["FieldDefinition", ...] = field(default_factory=tuple)
    is_collection: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    keyword_def: FieldKeywordDefinition = field(default_factory=FieldKeywordDefinition)


@dataclass(frozen=True)
class SegmentDefinition:
    name: str
    description: str | None = None
    fields: tuple[FieldDefinition, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocumentSegmentDefinition:
    doc_type: str
    segments: tuple[SegmentDefinition, ...]
    aliases: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


class SegmentDefinitionSource(Protocol):
    def get(self, doc_type: str) -> DocumentSegmentDefinition: ...

    def exists(self, doc_type: str) -> bool: ...
