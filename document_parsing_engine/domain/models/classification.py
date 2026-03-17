from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

class DocType(str, Enum):
    QUOTATION = "quotation"
    INVOICE = "invoice"
    PURCHASE_ORDER = "purchase_order"
    BILL_OF_LADING = "bill_of_lading"
    MTC = "mtc"
    UNKNOWN = "unknown"


@dataclass
class ClassificationResult:
    doc_type: DocType
    score: int
    reasons: List[str] = field(default_factory=list)
    all_scores: Dict[str, int] = field(default_factory=dict)
