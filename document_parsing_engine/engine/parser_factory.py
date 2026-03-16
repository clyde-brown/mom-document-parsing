"""문서 타입/벤더별 DocumentParser 생성. 빌드 로직은 여기로 집중."""

from document_parsing_engine.domain.parsers.document import (
    BaseDocumentParser,
    InvoiceDocumentParser,
)
from document_parsing_engine.domain.parsers.section import (
    GroupKVSectionParser,
    TableSectionParser,
)
from document_parsing_engine.domain.normalizers import InvoiceNormalizer
from document_parsing_engine.domain.validators import InvoiceValidator


class ParserFactory:
    """document_type, vendor에 따라 DocumentParser 인스턴스를 반환."""

    def __init__(self, presets=None):
        self.presets = presets or {}

    def get_document_parser(
        self,
        document_type: str | None = None,
        vendor: str | None = None,
    ) -> BaseDocumentParser:


        if document_type == "quotation":
        document_type = document_type or "invoice"
        if document_type == "invoice":
            return self._build_invoice_parser(vendor=vendor)
        raise ValueError(f"Unknown document_type: {document_type!r}")

    def _build_invoice_parser(self, vendor: str | None = None) -> InvoiceDocumentParser:
        from document_parsing_engine.presets.invoice import INVOICE_GROUP_KNOWN_KEYS

        section_parsers = [
            GroupKVSectionParser(known_keys=INVOICE_GROUP_KNOWN_KEYS),
            TableSectionParser(),
        ]
        return InvoiceDocumentParser(
            section_parsers=section_parsers,
            normalizer=InvoiceNormalizer(),
            validator=InvoiceValidator(),
        )
