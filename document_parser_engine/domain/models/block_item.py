from dataclasses import dataclass
from typing import Optional

from document_parsing_engine.domain.models.bbox import BBox


@dataclass
class BlockItem:
    ref: str
    text: str
    bbox: BBox
    page_no: int = 0
    label: Optional[str] = None
