"""추출 결과 정규화 서비스."""


class NormalizationService:
    def __init__(self, normalizer):
        self.normalizer = normalizer

    def normalize(self, extracted: dict) -> dict:
        if self.normalizer is None:
            return extracted
        return self.normalizer.normalize(extracted)
