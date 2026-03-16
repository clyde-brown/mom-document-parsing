import re


def normalize_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_key(key: str) -> str:
    key = normalize_text(key)
    key = key.replace(" :", "").strip()
    return key