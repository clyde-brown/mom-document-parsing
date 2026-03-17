from document_parsing_engine.app.services.document_classification_service import (
    DocumentClassificationService,
)
from document_parsing_engine.app.services.section_parsing_service import SectionParsingService
from document_parsing_engine.app.services.normalization_service import NormalizationService
from document_parsing_engine.app.services.validation_service import ValidationService

__all__ = [
    "BlockContent",
    "DocumentClassificationService",
    "DocumentLayoutParsingService",
    "SectionParsingService",
    "NormalizationService",
    "ValidationService",
]


def __getattr__(name: str):
    """Layout 파싱 서비스는 지연 로딩. 캐시된 패키지에서도 최신 모듈을 불러옴."""
    if name == "DocumentLayoutParsingService":
        from document_parsing_engine.app.services.document_layout_parsing_service import (
            DocumentLayoutParsingService,
        )
        return DocumentLayoutParsingService
    if name == "BlockContent":
        from document_parsing_engine.app.services.document_layout_parsing_service import (
            BlockContent,
        )
        return BlockContent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
