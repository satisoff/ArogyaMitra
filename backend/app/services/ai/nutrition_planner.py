from app.services.ai.groq_client import call_groq_json
from app.services.ai.nutrition_prompt_builder import build_nutrition_prompt


def generate_ai_nutrition_plan(
    calorie_target: int,
    dietary_preference: str,
    allergies: str | None,
):
    payload = build_nutrition_prompt(
        calorie_target=calorie_target,
        dietary_preference=dietary_preference,
        allergies=allergies,
    )

    try:
        result = call_groq_json(payload)
    except Exception:
        return {
            "days": [],
            "source": "fallback"
        }
    if not result.get("days") or len(result["days"]) != 7:
        return {
            "days": [],
            "source": "fallback"
        }

    result["source"] = "groq"
    return result 