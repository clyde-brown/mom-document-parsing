from abc import ABC, abstractmethod
from document_parser.core.models import ParseResult


class BaseDocumentParser(ABC):
    def __init__(self, section_parsers=None, normalizer=None, validator=None):
        self.section_parsers = section_parsers or []
        self.normalizer = normalizer
        self.validator = validator

    @abstractmethod
    def classify(self, doc: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def segment_sections(self, doc: dict):
        raise NotImplementedError

    def parse(self, doc: dict) -> ParseResult:
        document_type = self.classify(doc)
        sections = self.segment_sections(doc)

        extracted = {}
        debug = {"sections": []}

        for section in sections:
            parser = self._find_parser(section)
            if parser is None:
                continue

            parsed = parser.parse(doc, section)
            extracted[section.ref] = parsed
            debug["sections"].append({
                "ref": section.ref,
                "kind": section.kind,
                "parsed": parsed,
            })

        normalized = self.normalizer.normalize(extracted) if self.normalizer else extracted
        errors = self.validator.validate(normalized) if self.validator else []

        return ParseResult(
            document_type=document_type,
            sections=sections,
            extracted=extracted,
            normalized=normalized,
            validation_errors=errors,
            debug=debug,
        )

    def _find_parser(self, section):
        for parser in self.section_parsers:
            if parser.can_parse(section):
                return parser
        return None