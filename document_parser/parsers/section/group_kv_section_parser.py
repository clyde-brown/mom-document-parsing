from document_parser.parsers.section.base_section_parser import BaseSectionParser
from document_parser.layout.row_clusterer import RowClusterer
from document_parser.layout.zone_splitter import AdaptiveZoneSplitter
from document_parser.utils.refs import resolve_ref, get_first_prov
from document_parser.utils.text import normalize_text, normalize_key
from document_parser.core.models import BBox, BlockItem


class GroupKVSectionParser(BaseSectionParser):
    def __init__(
        self,
        y_tol: float = 10.0,
        min_gap_threshold: float = 18.0,
        gap_ratio: float = 1.8,
        known_keys: set | None = None,
        debug: bool = False,
    ):
        self.row_clusterer = RowClusterer(y_tol=y_tol)
        self.zone_splitter = AdaptiveZoneSplitter(
            min_threshold=min_gap_threshold,
            ratio=gap_ratio,
        )
        self.known_keys = known_keys
        self.debug = debug

    def can_parse(self, section) -> bool:
        return section.kind == "group_kv"

    def parse(self, doc: dict, section) -> dict:
        items = self._extract_items(doc, section.ref)
        rows = self.row_clusterer.cluster(items)

        kv_by_row = []
        for row in rows:
            zones = self.zone_splitter.split(row.items)
            row_kvs = [self._parse_zone(zone) for zone in zones]
            kv_by_row.append(row_kvs)

        return self._merge_rows(kv_by_row)

    def _extract_items(self, doc: dict, group_ref: str) -> list[BlockItem]:
        group_obj = resolve_ref(doc, group_ref)
        result = []

        for child in group_obj.get("children", []):
            ref = child.get("$ref")
            if not ref:
                continue

            obj = resolve_ref(doc, ref)
            text = normalize_text(obj.get("text", ""))
            prov = get_first_prov(obj)

            if not text or not prov or "bbox" not in prov:
                continue

            bbox = prov["bbox"]
            result.append(
                BlockItem(
                    ref=ref,
                    text=text,
                    bbox=BBox(
                        l=bbox["l"],
                        t=bbox["t"],
                        r=bbox["r"],
                        b=bbox["b"],
                        coord_origin=bbox.get("coord_origin", "BOTTOMLEFT"),
                    ),
                    page_no=prov.get("page_no", 0),
                    label=obj.get("label"),
                )
            )

        return result

    def _parse_zone(self, zone_items: list[BlockItem]):
        text = " ".join(x.text for x in zone_items)
        text = normalize_text(text)

        if " : " in text:
            key, value = text.split(" : ", 1)
            return normalize_key(key), normalize_text(value)

        if ":" in text:
            key, value = text.split(":", 1)
            return normalize_key(key), normalize_text(value)

        return normalize_key(text), ""

    def _merge_rows(self, rows_zone_kv):
        result = {}
        last_key = None

        for row in rows_zone_kv:
            for key, value in row:
                if not key:
                    if last_key and value:
                        result[last_key] = normalize_text(result[last_key] + " " + value)
                    continue

                if self.known_keys is not None and key not in self.known_keys and last_key:
                    append_text = normalize_text(f"{key} {value}".strip())
                    result[last_key] = normalize_text(result[last_key] + " " + append_text)
                    continue

                if key in result and value:
                    result[key] = normalize_text(result[key] + " " + value)
                else:
                    result[key] = value

                last_key = key

        return result