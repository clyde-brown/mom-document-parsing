"""
필드 매핑 서비스 (얇은 오케스트레이션).
입력: doc_type, seg(LayoutSegmentMappingRecommendation), blocks
출력: quotation_meta / items / remarks 구조의 JSON 호환 dict
"""

from __future__ import annotations

from typing import Any

from document_parsing_engine.app.services.document_layout_parsing_service import (
    BlockContent,
)
from document_parsing_engine.domain.field_mapping import (
    build_extraction_variables,
    parse_llm_response_to_output,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
)
from document_parsing_engine.llm import chat
from document_parsing_engine.prompt import get_extraction_prompts


class FieldMappingService:
    """세그먼트 매핑 결과 + 블록을 LLM으로 넘겨 필드 매핑 JSON을 반환."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
    ):
        self._model = model
        self._max_tokens = max_tokens

    def extract(
        self,
        doc_type: str,
        seg: LayoutSegmentMappingRecommendation,
        blocks: list[BlockContent],
    ) -> dict[str, Any]:
        """doc_type, seg(매핑 추천 결과), blocks를 사용해 필드 매핑 결과(JSON 호환 dict)를 반환.
        seg는 mapper.recommend() 반환값이어야 하며, segment_data가 아님.
        """
        variables = build_extraction_variables(doc_type, seg, blocks)
        system_prompt, user_prompt = get_extraction_prompts(variables)
        response_text = chat(
            system_prompt,
            user_prompt,
            model=self._model,
            max_tokens=self._max_tokens,
        )
        return parse_llm_response_to_output(response_text)
