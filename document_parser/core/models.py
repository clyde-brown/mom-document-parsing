from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BBox:
    l: float
    t: float
    r: float
    b: float
    coord_origin: str = "BOTTOMLEFT"


@dataclass
class BlockItem:
    ref: str
    text: str
    bbox: BBox
    page_no: int = 0
    label: Optional[str] = None


@dataclass
class Row:
    items: list[BlockItem] = field(default_factory=list)
    y: float = 0.0
    coord_origin: str = "BOTTOMLEFT"


@dataclass
class Section:
    ref: str
    label: str
    kind: str
    raw_obj: dict[str, Any]
    items: list[BlockItem] = field(default_factory=list)


@dataclass
class ParseResult:
    document_type: str
    sections: list[Section]
    extracted: dict[str, Any]
    normalized: dict[str, Any]
    validation_errors: list[str] = field(default_factory=list)
    debug: dict[str, Any] = field(default_factory=dict)