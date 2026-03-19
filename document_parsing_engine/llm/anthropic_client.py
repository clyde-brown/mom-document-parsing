"""Anthropic Claude API 호출 (시스템 + 유저 메시지)."""

from __future__ import annotations

from document_parsing_engine.llm.config import load_api_key


def chat(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    api_key: str | None = None,
) -> str:
    """시스템 프롬프트 + 유저 메시지로 Claude API를 호출하고 응답 텍스트를 반환."""
    key = api_key or load_api_key()
    if not key:
        raise ValueError(
            "ANTHROPIC_API_KEY를 환경 변수 또는 .env 파일에 설정하세요."
        )
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise ImportError("anthropic 패키지가 필요합니다: pip install anthropic") from e

    client = Anthropic(api_key=key)
    msg = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    if msg.content and len(msg.content) > 0:
        return (msg.content[0].text or "").strip()
    return ""
