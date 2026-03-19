"""문서 타입별 세그먼트 정의 preset (견적서, 발주서)."""

from document_parsing_engine.domain.models.segment_document_definition import (
    DocumentSegmentDefinition,
    FieldDefinition,
    FieldKeywordDefinition,
    SegmentDefinition,
)

QUOTATION_SEGMENT_DEFINITION = DocumentSegmentDefinition(
    doc_type="quotation",
    aliases=("steel_quotation", "quote"),
    segments=(
        SegmentDefinition(
            name="quotation_meta",
            description="견적서 상단 메타 정보 및 거래 당사자/거래 조건",
            metadata={
                "segment_keywords": ("견적서", "quotation", "quote"),
                "segment_keyword_boost_score": 0.12,
                "title_keywords": ("견적서", "quotation", "quote"),
                "title_boost_score": 0.22,
                "preferred_block_types": ("text", "group_kv"),
                "preferred_labels": ("section_header", "key_value_area", "text"),
            },
            fields=(
                FieldDefinition(
                    name="document_key",
                    description="문서 식별 키",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("견적번호", "no.", "문서번호", "document no"),
                        boost_score=0.08,
                    ),
                ),
                FieldDefinition(
                    name="supplier_name",
                    description="공급업체 상호",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("공급업체", "supplier", "판매처", "상호", "회사명","company name", "company"),
                        boost_score=0.05,
                    ),
                ),
                FieldDefinition(
                    name="supplier_contact_person",
                    description="공급업체 담당자명",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("담당자", "작성자", "수신", "contact person", "sales rep."),
                        boost_score=0.04,
                    ),
                ),
                FieldDefinition(
                    name="supplier_phone",
                    description="공급업체 연락처",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("tel", "전화", "연락처", "phone", "fax", "email", "e-mail"),
                        boost_score=0.04,
                    ),
                ),
                FieldDefinition(
                    name="supplier_address",
                    description="공급업체 주소",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("주소", "address"),
                        boost_score=0.03,
                    ),
                ),
                FieldDefinition(
                    name="buyer_name",
                    description="고객사 상호",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("수신", "귀중", "貴中", "buyer", "고객사", "company", "to"),
                        boost_score=0.05,
                    ),
                ),
                FieldDefinition(
                    name="buyer_contact_person",
                    description="고객사 담당자명",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("수신", "참조", "담당자","Reference"),
                        boost_score=0.04,
                    ),
                ),
                FieldDefinition(
                    name="buyer_phone",
                    description="고객사 연락처",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("tel", "전화", "연락처", "tel."),
                        boost_score=0.03,
                    ),
                ),
                FieldDefinition(
                    name="buyer_address",
                    description="고객사 주소",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("주소", "address"),
                        boost_score=0.03,
                    ),
                ),
                FieldDefinition(
                    name="validity",
                    description="견적 유효기간",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("유효기간", "validity"),
                        boost_score=0.07,
                    ),
                ),
                FieldDefinition(
                    name="payment_terms",
                    description="대금지급 조건",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("지불조건", "결제조건", "payment"),
                        boost_score=0.07,
                    ),
                ),
                FieldDefinition(
                    name="delivery_terms",
                    description="운송 조건",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("인도조건", "운송조건", "delivery", "납기일자"),
                        boost_score=0.07,
                    ),
                ),
            ),
        ),
        SegmentDefinition(
            name="items",
            description="품목 테이블 및 합계",
            metadata={
                "segment_keywords": ("품명", "재질", "규격", "수량", "단가", "금액", "합계"),
                "segment_keyword_boost_score": 0.10,
                "preferred_block_types": ("table",),
                "preferred_labels": ("table",),
            },
            fields=(
                FieldDefinition(
                    name="rows",
                    description="품목 행 목록",
                    is_collection=True,
                    data_type="object",
                    children=(
                        FieldDefinition(
                            name="unit_price",
                            description="단가",
                            data_type="number",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("단가", "unit price", "price"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="quantity",
                            description="수량",
                            data_type="number",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("수량", "qty", "q'ty", "quantity"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="line_amount",
                            description="행 금액",
                            data_type="number",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("금액", "amount"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="material_grade",
                            description="재질",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("재질", "grade", "material"),
                                boost_score=0.06,
                            ),
                        ),
                        FieldDefinition(
                            name="thickness",
                            description="두께",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("두께", "thickness"),
                                boost_score=0.05,
                            ),
                        ),
                        FieldDefinition(
                            name="size_text",
                            description="사이즈 원문",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("사이즈", "size", "길이", "폭", "length"),
                                boost_score=0.05,
                            ),
                        ),
                        FieldDefinition(
                            name="spec_text",
                            description="규격/스펙 원문",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("규격", "spec", "maker", "메이커", "description","material"),
                                boost_score=0.06,
                            ),
                        ),
                        FieldDefinition(
                            name="vat",
                            description="부가세",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("부가세", "vat", "세액"),
                                boost_score=0.05,
                            ),
                        ),
                    ),
                ),
                FieldDefinition(
                    name="totals",
                    description="합계 정보",
                    data_type="object",
                    children=(
                        FieldDefinition(
                            name="total_amount",
                            description="총액",
                            data_type="number",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("합계", "총액", "부가세", "vat", "합계금액"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="supply_amount",
                            description="공급가액",
                            data_type="number",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("공급가액", "공급가", "supply amount", "소계"),
                                boost_score=0.08,
                            ),
                        ),
                    ),
                ),
            ),
        ),
        SegmentDefinition(
            name="remarks",
            description="비고 및 자유 텍스트",
            metadata={
                "segment_keywords": ("특기사항", "비고", "remarks", "remark", "note", "특이사항","요청사항","필수요청사항","special request"),
                "segment_keyword_boost_score": 0.12,
                "title_keywords": ("특기사항", "비고", "remarks", "remark", "note", "특이사항","요청사항","필수요청사항","special request"),
                "title_boost_score": 0.20,
                "preferred_block_types": ("text", "group_kv"),
                "preferred_labels": ("section_header", "list", "text"),
            },
            fields=(
                FieldDefinition(
                    name="raw_text",
                    description="비고 원문",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("특기사항", "비고", "remark", "remarks", "note"),
                        boost_score=0.08,
                    ),
                ),
                FieldDefinition(
                    name="extracted_conditions",
                    description="추출된 조건 정보",
                    data_type="object",
                    required=False,
                    keyword_def=FieldKeywordDefinition(
                        keywords=("생산불가", "대체견적", "수급불가", "조건"),
                        boost_score=0.05,
                    ),
                ),
            ),
        ),
    ),
)

PURCHASE_ORDER_SEGMENT_DEFINITION = DocumentSegmentDefinition(
    doc_type="purchase_order",
    aliases=("po", "order_sheet"),
    segments=(
        SegmentDefinition(
            name="order_meta",
            description="발주서 상단 메타 정보",
            metadata={
                "segment_keywords": ("발주서", "purchase order", "po"),
                "segment_keyword_boost_score": 0.12,
                "title_keywords": ("발주서", "purchase order", "po"),
                "title_boost_score": 0.22,
                "preferred_block_types": ("text", "group_kv"),
                "preferred_labels": ("section_header", "key_value_area", "text"),
            },
            fields=(
                FieldDefinition(
                    name="order_no",
                    description="발주번호",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("발주번호", "order no", "po no"),
                        boost_score=0.08,
                    ),
                ),
                FieldDefinition(
                    name="supplier_name",
                    description="공급업체",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("공급업체", "supplier", "vendor"),
                        boost_score=0.05,
                    ),
                ),
                FieldDefinition(
                    name="buyer_name",
                    description="발주처",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("발주처", "buyer", "orderer"),
                        boost_score=0.05,
                    ),
                ),
            ),
        ),
        SegmentDefinition(
            name="items",
            description="발주 품목",
            metadata={
                "segment_keywords": ("품명", "수량", "단가", "금액"),
                "segment_keyword_boost_score": 0.10,
                "preferred_block_types": ("table",),
                "preferred_labels": ("table",),
            },
            fields=(
                FieldDefinition(
                    name="rows",
                    is_collection=True,
                    data_type="object",
                    children=(
                        FieldDefinition(
                            name="item_name",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("품명", "item"),
                                boost_score=0.06,
                            ),
                        ),
                        FieldDefinition(
                            name="quantity",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("수량", "qty", "quantity"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="unit_price",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("단가", "unit price"),
                                boost_score=0.08,
                            ),
                        ),
                        FieldDefinition(
                            name="line_amount",
                            keyword_def=FieldKeywordDefinition(
                                keywords=("금액", "amount"),
                                boost_score=0.08,
                            ),
                        ),
                    ),
                ),
            ),
        ),
        SegmentDefinition(
            name="remarks",
            description="비고",
            metadata={
                "segment_keywords": ("비고", "remarks", "note"),
                "segment_keyword_boost_score": 0.10,
                "title_keywords": ("비고", "remarks", "note"),
                "title_boost_score": 0.18,
                "preferred_block_types": ("text", "group_kv"),
                "preferred_labels": ("section_header", "text", "list"),
            },
            fields=(
                FieldDefinition(
                    name="raw_text",
                    keyword_def=FieldKeywordDefinition(
                        keywords=("비고", "remarks", "note"),
                        boost_score=0.08,
                    ),
                ),
            ),
        ),
    ),
)


def get_segment_definition(doc_type: str) -> DocumentSegmentDefinition:
    """doc_type(예: classification_result.doc_type.value)에 맞는 세그먼트 정의를 반환한다."""
    doc_type_lower = (doc_type or "").strip().lower()
    for definition in (QUOTATION_SEGMENT_DEFINITION, PURCHASE_ORDER_SEGMENT_DEFINITION):
        if definition.doc_type.lower() == doc_type_lower:
            return definition
        if doc_type_lower in (a.lower() for a in definition.aliases):
            return definition
    raise KeyError(
        f"Unknown doc_type: {doc_type!r}. Supported: quotation, purchase_order (and aliases)."
    )
