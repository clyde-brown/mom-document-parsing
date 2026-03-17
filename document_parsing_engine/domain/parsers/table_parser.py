"""테이블 블록에서 행/셀 텍스트 추출. Docling table data 형식에 의존."""


def get_table_rows(table_obj: dict) -> list[list[str]]:
    """
    table_obj["data"]["grid"]에서 행별 셀 텍스트 리스트 반환.
    """
    grid = (table_obj.get("data") or {}).get("grid", [])
    return [
        [(cell.get("text") or "").strip() for cell in row]
        for row in grid
    ]
