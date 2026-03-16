"""섹션별 파싱 위임 서비스."""

from document_parsing_engine.domain.models import Section
from document_parsing_engine.domain.parsers.section import BaseSectionParser


class SectionParsingService:
    def __init__(self, section_parsers: list[BaseSectionParser]):
        self.section_parsers = section_parsers

    def find_parser(self, section: Section) -> BaseSectionParser | None:
        for parser in self.section_parsers:
            if parser.can_parse(section):
                return parser
        return None

    def parse_section(self, doc: dict, section: Section) -> dict | None:
        parser = self.find_parser(section)
        if parser is None:
            return None
        return parser.parse(doc, section)
