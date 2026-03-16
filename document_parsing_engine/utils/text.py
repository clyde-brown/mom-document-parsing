import re


def normalize_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_key(key: str) -> str:
    key = normalize_text(key)
    key = key.replace(" :", "").strip()
    return key


class TextNormalizer:
    """분류/매칭용 정규화: 소문자 통일, 끝 콜론 제거."""

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""

        # 앞뒤 공백 제거
        text = text.strip()

        # 중간 다중 공백 정리
        text = " ".join(text.split())

        # 영어 대소문자 통일
        text = text.lower()

        # 끝의 콜론 제거
        text = re.sub(r"[:：]+$", "", text)

        # 끝 공백 제거
        return text.strip()
