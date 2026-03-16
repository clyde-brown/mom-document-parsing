"""정규화 결과 검증 서비스."""


class ValidationService:
    def __init__(self, validator):
        self.validator = validator

    def validate(self, normalized: dict) -> list[str]:
        if self.validator is None:
            return []
        return self.validator.validate(normalized)
