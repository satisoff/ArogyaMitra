from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.groq_client import GroqClientPlaceholder
from app.services.ai.prompt_builder import build_workout_prompt


def generate_ai_workout_outline(user: User, profile: HealthProfile) -> dict:
    """Return placeholder AI planner output for future Groq integration."""
    prompt = build_workout_prompt(user=user, profile=profile)
    client = GroqClientPlaceholder()
    return client.generate(prompt)
