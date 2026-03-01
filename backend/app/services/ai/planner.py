import logging

from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.groq_client import call_groq_json
from app.services.ai.prompt_builder import build_workout_prompt

logger = logging.getLogger(__name__)


def _is_valid_outline(data: dict) -> bool:
    if not isinstance(data, dict):
        return False

    days = data.get("days")
    if not isinstance(days, list) or len(days) != 7:
        return False

    for day in days:
        if not isinstance(day, dict):
            return False
        if "day" not in day or "focus" not in day:
            return False

    return True


def _mock_outline(user: User, profile: HealthProfile) -> dict:
    goal = user.fitness_goal or "general_fitness"
    return {
        "summary": f"Fallback outline for {goal} at {profile.workout_location}.",
        "days": [
            {"day": "Monday", "focus": "Full Body", "intensity": "moderate", "notes": "Technique first."},
            {"day": "Tuesday", "focus": "Cardio + Core", "intensity": "moderate", "notes": "Steady pace."},
            {"day": "Wednesday", "focus": "Lower Body", "intensity": "moderate", "notes": "Controlled reps."},
            {"day": "Thursday", "focus": "Mobility", "intensity": "low", "notes": "Recovery work."},
            {"day": "Friday", "focus": "Upper Body", "intensity": "moderate", "notes": "Form over load."},
            {"day": "Saturday", "focus": "Conditioning", "intensity": "high", "notes": "Short intervals."},
            {"day": "Sunday", "focus": "Active Recovery", "intensity": "low", "notes": "Light movement."},
        ],
        "source": "fallback_mock",
    }


def generate_ai_workout_outline(user: User, profile: HealthProfile, extra_context=None) -> dict:
    """Generate structured outline via Groq with safe fallback behavior."""
    prompt = build_workout_prompt(user=user, profile=profile, extra_context=extra_context)

    try:
        outline = call_groq_json(prompt)
    except Exception as exc:  # noqa: BLE001 - intentional safe fallback
        return _mock_outline(user=user, profile=profile)
    
    if not _is_valid_outline(outline):
            return _mock_outline(user=user, profile=profile)

    outline["source"] = "groq"
    return outline
