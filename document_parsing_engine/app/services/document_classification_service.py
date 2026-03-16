"""문서 분류: doc + hint(document_type) → document_type 반환."""


class DocumentClassificationService:
    def __init__(self, default_document_type: str = "invoice"):
        self.default_document_type = default_document_type

    def classify(self, doc: dict, document_type_hint: str | None = None) -> str:
        """문서와 선택적 힌트를 받아 document_type 문자열 반환. MVP에서는 힌트 우선."""
        if document_type_hint:
            return document_type_hint
        return self.default_document_type
