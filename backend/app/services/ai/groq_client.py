import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def generate_structured_workout_outline(prompt: str) -> dict:
    """Call Groq chat completion API and return parsed JSON outline."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    payload = {
        "model": GROQ_MODEL,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a workout planning assistant. "
                    "Return JSON only. Do not include markdown or extra text."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    logger.info("Calling Groq API for structured workout outline")
    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    if isinstance(content, dict):
        return content

    return json.loads(content)
