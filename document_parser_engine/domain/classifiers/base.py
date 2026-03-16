from abc import ABC, abstractmethod

from document_parsing_engine.domain.models.classification import ClassificationResult


class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, doc_dict: dict) -> ClassificationResult:
        raise NotImplementedError
