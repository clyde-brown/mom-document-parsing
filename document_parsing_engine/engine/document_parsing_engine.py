"""최상위 façade: parser_factory로 parser를 얻어 parse 위임."""


from document_parsing_engine.app.services import DocumentClassificationService
from document_parsing_engine.loaders.docling_loader import DoclingLoader


class DocumentParsingEngine:
    def __init__(self):
        self.loader = DoclingLoader()
        self.classifier = DocumentClassificationService() 

    def process(self, file_path: str):
        # 1. 문서 읽기
        doc_dict = self.loader.load(file_path)

        # 2. 문서 타입 분류
        classification = self.classifier.classify(doc_dict)

        return {
            "doc_type": classification.doc_type,
            "score": classification.score,
            "reasons": classification.reasons,
        }
