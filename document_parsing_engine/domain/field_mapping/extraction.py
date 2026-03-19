"""필드 매핑 추출: 프롬프트 변수 조립, LLM 응답 파싱."""

from __future__ import annotations

import json
import re
from typing import Any

from document_parsing_engine.domain.field_mapping.keywords import (
    build_segment_field_keywords,
)
from document_parsing_engine.domain.field_mapping.output_model import (
    FieldMappingOutput,
)
from document_parsing_engine.domain.field_mapping.segment_data import (
    build_segment_data,
)
from document_parsing_engine.domain.models.segment_mapping_result import (
    LayoutSegmentMappingRecommendation,
)


def build_extraction_variables(
    doc_type: str,
    recommendation: LayoutSegmentMappingRecommendation,
    blocks: list[Any],
) -> dict[str, str]:
    """LLM 프롬프트에 넣을 변수 dict. segment_field_mapping_metadata, segment_mapping_result_data."""
    segment_field_keywords = build_segment_field_keywords(doc_type)
    segment_data = build_segment_data(recommendation, blocks)
    return {
        "segment_field_mapping_metadata": json.dumps(
            segment_field_keywords, ensure_ascii=False, indent=2
        ),
        "segment_mapping_result_data": json.dumps(
            segment_data, ensure_ascii=False, indent=2
        ),
    }


def parse_llm_response_to_output(response_text: str) -> FieldMappingOutput:
    """LLM 응답 문자열에서 JSON만 추출해 FieldMappingOutput으로 반환.
    마크다운 코드블록(```json ... ```)이 있으면 그 내용만 파싱.
    """
    text = (response_text or "").strip()
    # ```json ... ``` 또는 ```\n...\n``` 제거 후 파싱
    code_block = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if code_block:
        text = code_block.group(1).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data
