"""YAML 프롬프트 템플릿 로드 및 {{변수}} 삽입."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


def load_prompt_template(
    yaml_path: str | Path,
    template_key: str,
) -> str:
    """YAML 파일에서 지정한 키의 template 문자열을 반환한다.
    예: load_prompt_template('field_mapping.yaml', 'post_analysis')
    """
    path = _resolve_yaml_path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt YAML not found: {path}")

    if yaml is None:
        raise ImportError("PyYAML이 필요합니다: pip install pyyaml")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if template_key not in data:
        raise KeyError(f"Template key '{template_key}' not found in {path}. Keys: {list(data.keys())}")
    block = data[template_key]
    if isinstance(block, dict) and "template" in block:
        return block["template"].strip()
    if isinstance(block, str):
        return block.strip()
    raise ValueError(f"Template '{template_key}' has no 'template' field or string value.")


def make_prompt(
    template: str,
    variables: dict[str, Any],
) -> str:
    """템플릿 문자열에서 {{변수명}}을 variables 값으로 치환한다.
    values는 str이거나 JSON 등 str()로 넣을 수 있는 값.
    """
    result = template
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        if placeholder not in result:
            continue
        text = value if isinstance(value, str) else str(value)
        result = result.replace(placeholder, text)
    return result


def _resolve_yaml_path(yaml_path: str | Path) -> Path:
    """상대 경로면 document_parsing_engine/prompt/ 기준으로 해석."""
    path = Path(yaml_path)
    if path.is_absolute():
        return path
    base = Path(__file__).resolve().parent
    return base / path.name if (not path.parent or path.parent.name == "") else base.parent / path


def load_system_user_prompts(
    yaml_path: str | Path = "extraction_prompts.yaml",
    prompt_key: str = "segment_field_extraction",
) -> tuple[str, str]:
    """YAML에서 시스템 프롬프트와 유저 프롬프트(템플릿)를 함께 로드한다.
    Returns:
        (system_prompt, user_template)
    유저 템플릿에는 {{변수}}가 있으므로 make_prompt(user_template, variables)로 완성한다.
    """
    path = _resolve_yaml_path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt YAML not found: {path}")

    if yaml is None:
        raise ImportError("PyYAML이 필요합니다: pip install pyyaml")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if prompt_key not in data:
        raise KeyError(f"Key '{prompt_key}' not found in {path}. Keys: {list(data.keys())}")
    block = data[prompt_key]
    if not isinstance(block, dict):
        raise ValueError(f"'{prompt_key}' must be a dict with 'system' and 'user' keys.")
    system = (block.get("system") or "").strip()
    user = (block.get("user") or "").strip()
    return system, user


def get_extraction_prompts(
    variables: dict[str, Any] | None = None,
) -> tuple[str, str]:
    """extraction_prompts.yaml의 segment_field_extraction을 로드한다.
    variables가 주어지면 유저 프롬프트에 변수를 삽입한 문자열을 반환하고,
    None이면 (system, user_template) 반환.
    Returns:
        (system_prompt, user_prompt 또는 user_template)
    """
    system, user_template = load_system_user_prompts()
    if variables is not None:
        return system, make_prompt(user_template, variables)
    return system, user_template
