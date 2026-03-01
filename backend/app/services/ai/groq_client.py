import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq_json(payload: dict) -> dict:
    """
    Generic Groq transport layer.
    No schema assumptions.
    Returns parsed JSON.
    """

    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a strict JSON generator. Return valid JSON only."
            },
            {
                "role": "user",
                "content": str(payload)
            }
        ],
        "temperature": 0.3,
    }

    response = requests.post(GROQ_URL, headers=headers, json=body, timeout=20)
    response.raise_for_status()

    import json
    import re

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    # Remove ```json ``` or ``` wrappers
    content = content.strip()

    if content.startswith("```"):
        content = re.sub(r"^```[a-zA-Z]*", "", content)
        content = content.rstrip("```").strip()

    return json.loads(content)