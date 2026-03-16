from document_parsing_engine.domain.models import Section, ParseResult
from document_parsing_engine.domain.parsers.document.base_document_parser import BaseDocumentParser


class InvoiceDocumentParser(BaseDocumentParser):
    """견적서/인보이스류 문서 파서. segment_sections는 preset 또는 외부에서 주입."""

    def classify(self, doc: dict) -> str:
        return "invoice"

    def segment_sections(self, doc: dict) -> list[Section]:
        """프리셋 없이 사용 시 빈 리스트. presets.invoice 등으로 섹션 정의 후 사용."""
        return []
