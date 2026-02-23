class GroqClientPlaceholder:
    """Placeholder client for future Groq LLaMA integration."""

    def generate(self, prompt: str) -> dict:
        return {
            "status": "placeholder",
            "message": "Groq API integration is not enabled yet.",
            "prompt": prompt,
        }
