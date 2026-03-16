from dataclasses import dataclass, field
from typing import Any

from document_parsing_engine.domain.models.block_item import BlockItem


@dataclass
class Section:
    ref: str
    label: str
    kind: str
    raw_obj: dict[str, Any]
    items: list[BlockItem] = field(default_factory=list)
