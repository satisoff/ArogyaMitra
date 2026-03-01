import json
from app.services.ai.groq_client import call_groq_json
from app.services.workout.planner import generate_workout_plan


def detect_intent_with_ai(message: str) -> dict:
    prompt = f"""
    You are a fitness assistant.

    Classify the user message into flags.

    Return ONLY JSON like:
    {{
    "travel": true/false,
    "injury": true/false,
    "low_time": true/false
    }}

    Message: "{message}"
    """

    try:
        result = call_groq_json(prompt)
        return {
            "travel": result.get("travel", False),
            "injury": result.get("injury", False),
            "low_time": result.get("low_time", False),
        }
    except Exception:
        return {"travel": False, "injury": False, "low_time": False}


def generate_aromi_response(user, profile, message: str):
    flags = detect_intent_with_ai(message)

    new_plan = None
    if any(flags.values()):
        new_plan = generate_workout_plan(user=user, profile=profile, context_flags=flags)

    coaching_text = (
        "Got it! I've adjusted your plan to keep you consistent and safe. "
        "Remember — progress comes from consistency, not perfection."
    )

    return {
        "message": coaching_text,
        "updated_plan": new_plan,
        "flags": flags,
    }