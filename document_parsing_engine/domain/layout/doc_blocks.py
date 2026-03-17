"""Docling export에서 블록 목록·그룹 텍스트 추출. Docling Parser에 의존 (doc_dict 형식)."""

from document_parsing_engine.utils.refs import resolve_ref, get_first_prov
from document_parsing_engine.utils.text import normalize_text


def get_blocks_sorted(doc: dict) -> list[tuple[str, dict]]:
    """
    doc_dict에서 body.children 순서대로 (ref, obj) 리스트 반환.
    body가 없으면 groups, tables, pictures를 순서대로 사용.
    """
    result: list[tuple[str, dict]] = []

    children = (doc.get("body") or doc.get("content") or {}).get("children", [])

    if children:
        for child in children:
            ref = child.get("$ref") or child.get("ref")
            if ref:
                try:
                    obj = resolve_ref(doc, ref)
                    result.append((ref, obj))
                except (KeyError, IndexError, TypeError):
                    continue
        return result

    # fallback: groups, tables, pictures 순
    for i, obj in enumerate(doc.get("groups", [])):
        ref = obj.get("self_ref") or f"#/groups/{i}"
        result.append((ref, obj))

    for i, obj in enumerate(doc.get("tables", [])):
        ref = obj.get("self_ref") or f"#/tables/{i}"
        result.append((ref, obj))

    for i, obj in enumerate(doc.get("pictures", [])):
        ref = obj.get("self_ref") or f"#/pictures/{i}"
        result.append((ref, obj))

    return result


def get_group_texts_in_order(doc: dict, group_obj: dict) -> list[str]:
    """그룹 children을 좌표 순으로 정렬한 뒤 텍스트만 리스트로 반환 (출력/폴백용)."""
    items: list[tuple[tuple, str, str]] = []

    for child in group_obj.get("children", []):
        ref = child.get("$ref")
        if not ref:
            continue
        obj = resolve_ref(doc, ref)
        text = normalize_text(obj.get("text", ""))
        prov = get_first_prov(obj)
        if not (prov and text):
            continue
        bbox = prov.get("bbox", {})
        coord_origin = bbox.get("coord_origin", "BOTTOMLEFT")
        l_val = bbox.get("l", 999999)
        t_val = bbox.get("t", 999999)
        sort_key = (-t_val, l_val) if coord_origin == "BOTTOMLEFT" else (t_val, l_val)
        items.append((sort_key, text, ref))

    items.sort(key=lambda x: x[0])
    return [text for _, text, _ in items]
