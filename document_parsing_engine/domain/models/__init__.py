"""Domain models."""

from document_parsing_engine.domain.models.bbox import BBox
from document_parsing_engine.domain.models.block_item import BlockItem
from document_parsing_engine.domain.models.classification import (
    ClassificationResult,
    DocType,
)
from document_parsing_engine.domain.models.row import Row
from document_parsing_engine.domain.models.section import Section
from document_parsing_engine.domain.models.parse_result import ParseResult
from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
    FieldDefinition,
    FieldKeywordDefinition,
    SegmentDefinition,
    SegmentDefinitionSource,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    BlockSegmentRecommendation,
    LayoutSegmentMappingRecommendation,
    SegmentBucket,
    SegmentCandidate,
)

__all__ = [
    "BBox",
    "BlockItem",
    "BlockSegmentRecommendation",
    "ClassificationResult",
    "DocType",
    "DocumentSegmentDefinition",
    "FieldDefinition",
    "FieldKeywordDefinition",
    "LayoutSegmentMappingRecommendation",
    "Row",
    "SegmentBucket",
    "SegmentCandidate",
    "SegmentDefinition",
    "SegmentDefinitionSource",
    "Section",
    "ParseResult",
]
