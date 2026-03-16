"""최상위 façade: parser_factory로 parser를 얻어 parse 위임."""

from document_parsing_engine.domain.models import ParseResult
from document_parsing_engine.domain.parsers.document import BaseDocumentParser


class DocumentParsingEngine:
    def __init__(self, parser_factory):
        self.parser_factory = parser_factory

    def parse(
        self,
        doc_dict: dict,
        document_type: str | None = None,
        vendor: str | None = None,
    ) -> ParseResult:
        parser: BaseDocumentParser = self.parser_factory.get_document_parser(
            document_type=document_type,
            vendor=vendor,
        )
        return parser.parse(doc_dict)
