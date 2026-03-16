from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ClassificationResult:
    doc_type: str
    score: int
    reasons: List[str] = field(default_factory=list)
    all_scores: Dict[str, int] = field(default_factory=dict)
