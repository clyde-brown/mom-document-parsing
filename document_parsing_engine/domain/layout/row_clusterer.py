from document_parsing_engine.domain.models import Row, BlockItem


class RowClusterer:
    def __init__(self, y_tol: float = 10.0):
        self.y_tol = y_tol

    def cluster(self, items: list[BlockItem]) -> list[Row]:
        if not items:
            return []

        items_sorted = sorted(items, key=self._sort_key)
        rows: list[Row] = []

        for item in items_sorted:
            placed = False
            for row in rows:
                if row.coord_origin != item.bbox.coord_origin:
                    continue
                if abs(row.y - item.bbox.t) <= self.y_tol:
                    row.items.append(item)
                    row.y = sum(x.bbox.t for x in row.items) / len(row.items)
                    placed = True
                    break

            if not placed:
                rows.append(
                    Row(
                        items=[item],
                        y=item.bbox.t,
                        coord_origin=item.bbox.coord_origin,
                    )
                )

        for row in rows:
            row.items = sorted(row.items, key=lambda x: x.bbox.l)

        rows = sorted(rows, key=lambda r: self._row_sort_key(r))
        return rows

    def _sort_key(self, item: BlockItem):
        if item.bbox.coord_origin == "BOTTOMLEFT":
            return (item.page_no, -item.bbox.t, item.bbox.l)
        return (item.page_no, item.bbox.t, item.bbox.l)

    def _row_sort_key(self, row: Row):
        first = row.items[0]
        if row.coord_origin == "BOTTOMLEFT":
            return (first.page_no, -row.y, min(x.bbox.l for x in row.items))
        return (first.page_no, row.y, min(x.bbox.l for x in row.items))
