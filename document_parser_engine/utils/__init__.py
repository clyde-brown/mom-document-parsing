"""Utilities."""

from document_parsing_engine.utils.refs import resolve_ref, get_first_prov
from document_parsing_engine.utils.text import (
    normalize_text,
    normalize_key,
    TextNormalizer,
)

__all__ = [
    "resolve_ref",
    "get_first_prov",
    "normalize_text",
    "normalize_key",
    "TextNormalizer",
]
