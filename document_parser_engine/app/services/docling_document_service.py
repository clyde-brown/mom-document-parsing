"""문서 전체를 다루는 서비스. classifier 호출."""

from document_parsing_engine.domain.classifiers.doc_type_classifier import DocTypeClassifier
from document_parsing_engine.domain.models.classification import ClassificationResult


class DoclingDocumentService:
    def __init__(self):
        self.doc_type_classifier = DocTypeClassifier()

    def classify_doc_type(self, doc_dict: dict) -> ClassificationResult:
        return self.doc_type_classifier.classify(doc_dict)
