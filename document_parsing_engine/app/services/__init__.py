from document_parsing_engine.app.services.document_classification_service import (
    DocumentClassificationService,
)
from document_parsing_engine.app.services.section_parsing_service import (
    SectionParsingService,
)
from document_parsing_engine.app.services.normalization_service import (
    NormalizationService,
)
from document_parsing_engine.app.services.validation_service import ValidationService

__all__ = [
    "BlockContent",
    "DocumentClassificationService",
    "DocumentLayoutParsingService",
    "LayoutSegmentMappingService",
    "SectionParsingService",
    "NormalizationService",
    "ValidationService",
]


def __getattr__(name: str):
    """Layout/segment 매핑 서비스는 지연 로딩."""
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
    if name == "LayoutSegmentMappingService":
        from document_parsing_engine.app.services.layout_segment_mapping_service import (
            LayoutSegmentMappingService,
        )

        return LayoutSegmentMappingService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
