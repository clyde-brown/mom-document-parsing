from dataclasses import dataclass, field

from document_parsing_engine.domain.models.block_item import BlockItem


@dataclass
class Row:
    items: list[BlockItem] = field(default_factory=list)
    y: float = 0.0
    coord_origin: str = "BOTTOMLEFT"
