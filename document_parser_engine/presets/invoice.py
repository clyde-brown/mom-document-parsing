"""견적서/인보이스용 프리셋. preset/template hint용 known keys."""

from document_parsing_engine.engine import DocumentParsingEngine, ParserFactory


INVOICE_GROUP_KNOWN_KEYS = frozenset({
    "견적 일자",
    "견적번호",
    "납기일자",
    "납기조건",
    "수신",
    "수신처",
    "발신",
    "발신처",
    "프로젝트",
    "참조",
    "의뢰번호",
    "인도조건",
    "지불조건",
    "유효기간",
    "합계금액",
    "VAT포함",
    "작성자",
    "Fax",
    "Tel",
    "E-mail",
})


def create_invoice_engine() -> DocumentParsingEngine:
    """ParserFactory를 사용하는 DocumentParsingEngine 반환. parse(doc, document_type='invoice') 사용."""
    return DocumentParsingEngine(parser_factory=ParserFactory())
