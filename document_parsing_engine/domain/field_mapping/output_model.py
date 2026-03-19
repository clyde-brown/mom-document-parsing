"""필드 매핑 LLM 출력 스키마 (quotation 등)."""

from __future__ import annotations

from typing import Any, TypedDict


class QuotationMeta(TypedDict, total=False):
    document_key: str
    supplier_name: str
    supplier_contact_person: str
    supplier_phone: str
    supplier_address: str
    buyer_name: str
    buyer_contact_person: str
    buyer_phone: str
    buyer_address: str
    validity: str
    payment_terms: str
    delivery_terms: str


class ItemRow(TypedDict, total=False):
    unit_price: int | float | None
    quantity: int | None
    line_amount: int | float | None
    vat: int | float | None
    material_grade: str
    thickness: str
    size_text: str
    spec_text: str


class ItemsTotals(TypedDict, total=False):
    supply_amount: int | float | None
    total_amount: int | float | None


class Items(TypedDict, total=False):
    rows: list[ItemRow]
    totals: ItemsTotals


class Remarks(TypedDict, total=False):
    raw_text: str
    extracted_conditions: list[str]


class FieldMappingOutput(TypedDict, total=False):
    """견적서 필드 매핑 최종 출력 (LLM 응답 파싱 결과)."""
    quotation_meta: QuotationMeta
    items: Items
    remarks: Remarks
