class AdaptiveZoneSplitter:
    def __init__(self, min_threshold: float = 18.0, ratio: float = 1.8):
        self.min_threshold = min_threshold
        self.ratio = ratio

    def split(self, row_items: list):
        if not row_items:
            return []

        items = sorted(row_items, key=lambda x: x.bbox.l)

        if len(items) == 1:
            return [items]

        gaps = []
        for prev, curr in zip(items, items[1:]):
            gap = max(0, curr.bbox.l - prev.bbox.r)
            gaps.append(gap)

        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        threshold = max(self.min_threshold, avg_gap * self.ratio)

        zones = []
        current_zone = [items[0]]

        for i, curr in enumerate(items[1:]):
            prev = items[i]
            gap = max(0, curr.bbox.l - prev.bbox.r)

            if gap >= threshold:
                zones.append(current_zone)
                current_zone = [curr]
            else:
                current_zone.append(curr)

        zones.append(current_zone)
        return zones