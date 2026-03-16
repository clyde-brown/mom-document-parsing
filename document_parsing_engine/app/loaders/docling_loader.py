from pathlib import Path


class DoclingLoader:
    def load(self, file_path: str) -> dict:
        """
        PDF / 이미지 문서를 Docling으로 파싱하여
        texts, tables, pictures 등의 구조화된 dict를 반환
        """
        path = Path(file_path)

        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        result = converter.convert(path)

        return result.document.export_to_dict()
