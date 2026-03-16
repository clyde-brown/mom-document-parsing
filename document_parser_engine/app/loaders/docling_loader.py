from pathlib import Path


class DoclingLoader:
    """PDF/이미지 문서를 Docling으로 파싱하여 구조화된 dict 반환."""

    def load(self, file_path: str) -> dict:
        """
        PDF / 이미지 문서를 Docling으로 파싱하여
        texts, tables, pictures 등의 구조화된 dict를 반환
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        result = converter.convert(path)

        return result.document.export_to_dict()
