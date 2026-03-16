from dataclasses import dataclass


@dataclass
class BBox:
    l: float
    t: float
    r: float
    b: float
    coord_origin: str = "BOTTOMLEFT"
