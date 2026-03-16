from dataclasses import dataclass, field
from typing import Any

from document_parsing_engine.domain.models.section import Section


@dataclass
class ParseResult:
    document_type: str
    sections: list[Section]
    extracted: dict[str, Any]
    normalized: dict[str, Any]
    validation_errors: list[str] = field(default_factory=list)
    debug: dict[str, Any] = field(default_factory=dict)
