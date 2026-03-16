from document_parsing_engine.domain.parsers.section.base_section_parser import BaseSectionParser


class TableSectionParser(BaseSectionParser):
    """테이블 형태 섹션 파서. 행/열 구조로 추출."""

    def can_parse(self, section) -> bool:
        return section.kind == "table"

    def parse(self, doc: dict, section) -> dict:
        """테이블 데이터를 리스트 of dict 또는 행 리스트로 반환."""
        return {"rows": [], "headers": []}
