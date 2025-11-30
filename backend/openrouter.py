"""Wrapper around the OpenRouter chat completion endpoint."""

from __future__ import annotations

import json
import os
import re
from typing import Dict, Optional

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # python-dotenv is optional (it may not be installed within Vercel)
    pass

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"


class OpenRouterError(RuntimeError):
    """Raised when the OpenRouter call fails."""


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise OpenRouterError(
            f"Missing environment variable {var_name}. "
            "Add it to your local .env and Vercel project settings."
        )
    return value.strip()


def grade_answer(
    *,
    question: str,
    standard_answer: str,
    user_answer: str,
    site_url: Optional[str] = None,
    app_name: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    timeout: int = 20,
) -> Dict[str, object]:
    """
    Call OpenRouter with the same rubric used in the Tkinter client.

    Returns a dict with the numeric score and textual feedback.
    """

    api_key = _require_env("OPENROUTER_API_KEY")
    site_url = site_url or os.getenv("YOUR_SITE_URL") or "https://localhost"
    app_name = app_name or os.getenv("YOUR_APP_NAME") or "Double Spin Wheel"

    prompt = f"""
You are an encouraging and supportive teacher. Be objective and fair; do not be
overly strict about formatting. If the standard answer is a placeholder like
"Personal Answer", give an objective score based solely on the student answer.

Question: {question}
Standard Answer: {standard_answer}
Student Answer: {user_answer}

Task:
1. Rate the student answer from 0 to 10.
2. Provide a very short feedback (max 2 sentences).

Respond strictly as JSON:
{{
    "score": <number>,
    "feedback": "<text>"
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": site_url,
        "X-Title": app_name,
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=timeout,
    )

    if response.status_code != 200:
        raise OpenRouterError(
            f"OpenRouter error {response.status_code}: {response.text}"
        )

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    match = re.search(r"\{.*\}", content, flags=re.DOTALL)
    parsed = {}
    if match:
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    score = int(parsed.get("score", 0))
    feedback = parsed.get("feedback", content.strip())

    return {
        "score": score,
        "feedback": feedback,
        "rawResponse": content,
    }

