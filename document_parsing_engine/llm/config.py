"""LLM API 키 등 설정 로드. .env 또는 지정 경로 파일에서 로드."""

from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # type: ignore[assignment, misc]


def load_api_key(
    env_var: str = "ANTHROPIC_API_KEY",
    dotenv_path: str | Path | None = None,
) -> str:
    """환경 변수에서 API 키를 읽는다. dotenv_path가 있으면 해당 파일을 먼저 로드.
    기본으로 프로젝트 루트의 .env 를 찾아 로드한다.
    """
    if load_dotenv is not None:
        if dotenv_path is not None:
            path = Path(dotenv_path)
            if path.exists():
                load_dotenv(path, override=False)
        else:
            # 프로젝트 루트: document_parsing_engine 상위까지 올라가 .env 탐색
            base = Path(__file__).resolve().parent
            for _ in range(4):
                base = base.parent
                env_file = base / ".env"
                if env_file.exists():
                    load_dotenv(env_file, override=False)
                    break
    return os.environ.get(env_var, "").strip()
