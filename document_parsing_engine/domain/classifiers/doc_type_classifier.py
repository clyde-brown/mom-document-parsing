from collections import defaultdict
from typing import Dict, List

from document_parsing_engine.domain.classifiers.base import BaseClassifier
from document_parsing_engine.domain.classifiers.rules import DOC_TYPE_RULES
from document_parsing_engine.domain.models.classification import (
    ClassificationResult,
    DocType,
)
from document_parsing_engine.utils.text import TextNormalizer


class DocTypeClassifier(BaseClassifier):
    def classify(self, doc_dict: dict) -> ClassificationResult:
        scores = defaultdict(int)
        reasons = defaultdict(list)

        texts = self._collect_texts(doc_dict)
        table_texts = self._collect_table_texts(doc_dict)

        for doc_type, rule in DOC_TYPE_RULES.items():
            self._apply_title_exact_rule(doc_type, rule, texts, scores, reasons)
            self._apply_text_contains_rule(doc_type, rule, texts, scores, reasons)
            self._apply_meta_fields_rule(doc_type, rule, texts, scores, reasons)
            self._apply_table_headers_rule(doc_type, rule, table_texts, scores, reasons)

        if not scores:
            return ClassificationResult(
                doc_type=DocType.UNKNOWN,
                score=0,
                reasons=[],
                all_scores={},
            )

        best_doc_type = max(scores, key=scores.get)
        best_score = scores[best_doc_type]

        if best_score <= 0:
            return ClassificationResult(
                doc_type=DocType.UNKNOWN,
                score=0,
                reasons=[],
                all_scores=dict(scores),
            )

        return ClassificationResult(
            doc_type=DocType(best_doc_type),
            score=best_score,
            reasons=reasons[best_doc_type],
            all_scores=dict(scores),
        )

    def _collect_texts(self, doc_dict: dict) -> List[dict]:
        result = []

        for t in doc_dict.get("texts", []):
            raw_text = t.get("text", "")
            norm_text = TextNormalizer.normalize(raw_text)

            result.append(
                {
                    "raw": raw_text,
                    "norm": norm_text,
                    "label": t.get("label"),
                    "prov": t.get("prov", []),
                }
            )

        return result

    def _collect_table_texts(self, doc_dict: dict) -> List[str]:
        values = []

        for table in doc_dict.get("tables", []):
            data = table.get("data", {})
            for cell in data.get("table_cells", []):
                raw_text = cell.get("text", "")
                norm_text = TextNormalizer.normalize(raw_text)
                if norm_text:
                    values.append(norm_text)

        return values

    def _apply_title_exact_rule(
        self,
        doc_type: str,
        rule: Dict,
        texts: List[dict],
        scores: defaultdict,
        reasons: defaultdict,
    ) -> None:
        candidates = set(rule.get("title_exact", []))

        for t in texts:
            if t["norm"] in candidates:
                if t.get("label") == "section_header":
                    scores[doc_type] += 10
                    reasons[doc_type].append(
                        f'title exact match(section_header): "{t["raw"]}"'
                    )
                else:
                    scores[doc_type] += 6
                    reasons[doc_type].append(f'title exact match: "{t["raw"]}"')

    def _apply_text_contains_rule(
        self,
        doc_type: str,
        rule: Dict,
        texts: List[dict],
        scores: defaultdict,
        reasons: defaultdict,
    ) -> None:
        candidates = rule.get("text_contains", [])

        for t in texts:
            for keyword in candidates:
                if keyword in t["norm"]:
                    scores[doc_type] += 2
                    reasons[doc_type].append(f'text contains "{keyword}": "{t["raw"]}"')

    def _apply_meta_fields_rule(
        self,
        doc_type: str,
        rule: Dict,
        texts: List[dict],
        scores: defaultdict,
        reasons: defaultdict,
    ) -> None:
        candidates = rule.get("meta_fields", [])

        for t in texts:
            for field_name in candidates:
                if field_name in t["norm"]:
                    scores[doc_type] += 3
                    reasons[doc_type].append(f'meta field "{field_name}": "{t["raw"]}"')

    def _apply_table_headers_rule(
        self,
        doc_type: str,
        rule: Dict,
        table_texts: List[str],
        scores: defaultdict,
        reasons: defaultdict,
    ) -> None:
        candidates = rule.get("table_headers", [])

        for cell_text in table_texts:
            for header in candidates:
                if header in cell_text:
                    scores[doc_type] += 2
                    reasons[doc_type].append(f'table header "{header}": "{cell_text}"')
