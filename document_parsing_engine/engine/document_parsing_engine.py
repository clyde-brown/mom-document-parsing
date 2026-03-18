"""최상위 façade: loader → classifier → layout → segment mapping."""

from document_parsing_engine.app.services import (
    DocumentClassificationService,
    DocumentLayoutParsingService,
    LayoutSegmentMappingService,
)
from document_parsing_engine.loaders.docling_loader import DoclingLoader


def _doc_type_str(doc_type):
    if hasattr(doc_type, "value"):
        return str(doc_type.value)
    return str(doc_type)


class DocumentParsingEngine:
    def __init__(self):
        self.loader = DoclingLoader()
        self.classifier = DocumentClassificationService()
        self.layout_parser = DocumentLayoutParsingService()
        self.segment_mapping = LayoutSegmentMappingService()

    def process(self, file_path: str):
        ## 1. 문서 읽기 (DoclingParser)
        doc_dict = self.loader.load(file_path)

        # 2. 문서 타입 분류
        classification = self.classifier.classify_doc_type(doc_dict)

        # 3. layout parsing
        blocks = self.layout_parser.parse_layout(doc_dict)

        # 4. segment mapping (철감문서 도메인 별 허용 segment 집합 추천)
        segment_result = self.segment_mapping.recommend(
            doc_type=classification.doc_type.value,
            doc_dict=doc_dict,
            blocks=blocks,
        )

        return {
            "doc_type": classification.doc_type,
            "score": classification.score,
            "reasons": classification.reasons,
            "segment_mapping": segment_result,
        }


# class DocumentParsingEngine:
#     def __init__(self, document_classification_service,
#             layout_analysis_service,
#             section_segmentation_service,
#             section_parsing_service,
#             reconstruction_service,
#             field_extraction_service,
#             normalization_service,
#             validation_service,
#             review_service,
#         ):
#         self.document_classification_service=document_classification_service
#         self.layout_analysis_service=layout_analysis_service
#         self.section_segmentation_service=section_segmentation_service
#         self.section_parsing_service=section_parsing_service
#         self.reconstruction_service=reconstruction_service
#         self.field_extraction_service=field_extraction_service
#         self.normalization_service=normalization_service
#         self.validation_service=validation_service
#         self.review_service=review_service

#     def parse(self,parsed_document,options=None):
#         document_type=self.document_classification_service.classify(parsed_document,options)
#         layout_result=self.layout_analysis_service.analyze(parsed_document,document_type,options)
#         sections=self.section_segmentation_service.segment(parsed_document,layout_result,document_type,options)
#         parsed_sections=self.section_parsing_service.parse_sections(parsed_document,sections,document_type,options)
#         reconstructed=self.reconstruction_service.reconstruct(parsed_sections,document_type,options)
#         extracted=self.field_extraction_service.extract(reconstructed,document_type,options)
#         normalized=self.normalization_service.normalize(extracted,document_type,options)
#         validation=self.validation_service.validate(normalized,document_type,options)
#         review=self.review_service.build_review_if_needed(parsed_document,document_type,validation,normalized)

#         return {
#         "document_type":document_type,
#         "sections":sections,
#         "normalized":normalized,
#         "validation":validation,
#         "review":review,
#                 }
