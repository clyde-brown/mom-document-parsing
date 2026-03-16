def resolve_ref(doc: dict, ref: str) -> dict:
    if ref.startswith("#/"):
        ref = ref[2:]
    elif ref.startswith("/"):
        ref = ref[1:]

    cur = doc
    for p in ref.split("/"):
        cur = cur[int(p)] if p.isdigit() else cur[p]
    return cur


def get_first_prov(obj: dict):
    prov = obj.get("prov") or []
    return prov[0] if prov else None