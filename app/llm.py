"""
OpenAI client wrapper. Reads OPENAI_API_KEY from environment.
Model configurable via OPENAI_MODEL (default: gpt-4o-mini).
"""

import os
from typing import Any

from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client


def get_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def complete(
    messages: list[dict[str, Any]],
    max_tokens: int = 500,
    temperature: float = 0.3,
) -> str:
    """
    Call OpenAI Chat Completions. Returns the assistant message content.
    Raises RuntimeError if API key is missing; propagates OpenAI errors.
    """
    client = _get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""
