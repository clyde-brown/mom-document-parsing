"""정의 소스: 코드 상수 기반 InMemory, Provider."""

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
    SegmentDefinitionSource,
)
from document_parsing_engine.domain.presets.segment_definitions import (
    PURCHASE_ORDER_SEGMENT_DEFINITION,
    QUOTATION_SEGMENT_DEFINITION,
)


class InMemorySegmentDefinitionSource:
    """코드에 정의된 문서 타입 정의 제공. DB 등 다른 소스로 교체 가능."""

    def __init__(self) -> None:
        definitions = (
            QUOTATION_SEGMENT_DEFINITION,
            PURCHASE_ORDER_SEGMENT_DEFINITION,
        )
        self._definitions_by_key: dict[str, DocumentSegmentDefinition] = {}
        for definition in definitions:
            self._register(definition)

    def _register(self, definition: DocumentSegmentDefinition) -> None:
        self._definitions_by_key[self._normalize(definition.doc_type)] = definition
        for alias in definition.aliases:
            self._definitions_by_key[self._normalize(alias)] = definition

    def get(self, doc_type: str) -> DocumentSegmentDefinition:
        normalized = self._normalize(doc_type)
        if normalized not in self._definitions_by_key:
            raise KeyError(f"Unsupported doc_type: {doc_type}")
        return self._definitions_by_key[normalized]

    def exists(self, doc_type: str) -> bool:
        return self._normalize(doc_type) in self._definitions_by_key

    @staticmethod
    def _normalize(doc_type: str) -> str:
        return doc_type.strip().lower()


class SegmentDefinitionProvider:
    """서비스는 source가 파일/코드/DB 중 어디인지 모르고 provider.get(doc_type)만 호출."""

    def __init__(
        self,
        source: SegmentDefinitionSource | None = None,
    ) -> None:
        self._source = source or InMemorySegmentDefinitionSource()

    def get(self, doc_type: str) -> DocumentSegmentDefinition:
        return self._source.get(doc_type)

    def exists(self, doc_type: str) -> bool:
        return self._source.exists(doc_type)
