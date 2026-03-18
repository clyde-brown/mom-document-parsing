"""doc_type별 대표 신호 정의."""

"""
추후 DB에서 값을 가져오도록 수정할 예정. -> 동적으로 업데이트 가능
"""


DOC_TYPE_RULES = {
    "quotation": {
        "title_exact": [
            "견적서",
            "見積書",
            "quotation",
            "estimate",
        ],
        "text_contains": [
            "견적",
            "見積",
        ],
        "meta_fields": [
            "견적 일자",
            "유효기간",
            "지불조건",
            "인도조건",
            "합계금액",
            "vat포함",
        ],
        "table_headers": [
            "단가",
            "unit price",
            "금액",
            "amount",
            "품명",
            "규격",
        ],
    },
    "invoice": {
        "title_exact": [
            "invoice",
            "commercial invoice",
            "세금계산서",
            "tax invoice",
            "거래명세서",
            "거래명세표",
        ],
        "text_contains": [
            "invoice",
            "세금계산서",
        ],
        "meta_fields": [
            "invoice no",
            "invoice date",
            "공급가액",
            "세액",
            "사업자등록번호",
        ],
        "table_headers": [
            "description",
            "quantity",
            "unit price",
            "amount",
        ],
    },
    "purchase_order": {
        "title_exact": [
            "발주서",
            "구매주문서",
            "purchase order",
            "p.o",
        ],
        "text_contains": [
            "발주",
        ],
        "meta_fields": [
            "발주번호",
            "납품처",
            "납품일",
        ],
        "table_headers": [
            "발주수량",
            "단가",
            "납기",
        ],
    },
    "bill_of_lading": {
        "title_exact": [
            "bill of lading",
            "b/l",
            "선하증권",
        ],
        "text_contains": [
            "bill of lading",
            "b/l",
            "선하증권",
        ],
        "meta_fields": [
            "shipper",
            "consignee",
            "port of loading",
            "port of discharge",
        ],
        "table_headers": [],
    },
    "mtc": {
        "title_exact": [
            "mill test certificate",
            "material test certificate",
        ],
        "text_contains": [
            "test certificate",
            "heat no",
        ],
        "meta_fields": [
            "heat no",
            "chemical composition",
            "mechanical properties",
        ],
        "table_headers": [
            "chemical composition",
            "mechanical properties",
        ],
    },
}
