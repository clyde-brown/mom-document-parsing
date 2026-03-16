"""견적서/인보이스 추출 결과 정규화 (날짜, 금액, 키 이름 등)."""


class InvoiceNormalizer:
    def normalize(self, extracted: dict) -> dict:
        """extracted: section ref -> parsed dict. 정규화된 구조로 반환."""
        return dict(extracted)
