import json

from app.models.health_profile import HealthProfile
from app.models.user import User


def build_workout_prompt(user: User, profile: HealthProfile, extra_context=None) -> str:
    """Build a structured JSON request prompt for workout outline generation."""
    request_payload = {
        "task": "generate_structured_workout_outline",
        "constraints": {
            "goal": user.fitness_goal or "general_fitness",
            "activity_level": profile.activity_level,
            "workout_location": profile.workout_location,
            "available_minutes_per_day": profile.available_minutes_per_day,
            "injuries": profile.injuries or "none",
        },
        "extra_context": extra_context or {},
        "response_schema": {
            "summary": "string",
            "days": [
                {
                    "day": "string",
                    "focus": "string",
                    "intensity": "low|moderate|high",
                    "notes": "string",
                }
            ],
        },
        "rules": [
            "Return valid JSON only.",
            "Return exactly 7 day objects in days.",
            "Keep recommendations aligned with injuries and workout location.",
        ],
    }
    return json.dumps(request_payload, ensure_ascii=False)
