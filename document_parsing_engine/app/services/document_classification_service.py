"""문서 분류 서비스. Docling Parser에 의존한다 (doc_dict는 Docling export_to_dict() 형식)."""

from document_parsing_engine.domain.classifiers.doc_type_classifier import DocTypeClassifier
from document_parsing_engine.domain.models.classification import ClassificationResult


class DocumentClassificationService:
    """Docling Parser에 의존: doc_dict는 Docling의 export_to_dict() 형식이어야 함."""

    def __init__(self):
        self.doc_type_classifier = DocTypeClassifier()

    def classify(self, doc_dict: dict) -> ClassificationResult:
        """Docling export_to_dict() 형식의 doc_dict를 분류. BaseClassifier API와 동일."""
        return self.doc_type_classifier.classify(doc_dict)

