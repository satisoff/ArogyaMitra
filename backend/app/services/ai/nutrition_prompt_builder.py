def build_nutrition_prompt(
    calorie_target: int,
    dietary_preference: str,
    allergies: str | None,
):
    return {
        "task": "generate_7_day_meal_plan",
        "constraints": {
            "calories_per_day": calorie_target,
            "dietary_preference": dietary_preference,
            "allergies": allergies or "none",
            "cuisine": "Indian",
        },
        "response_schema": {
            "days": [
                {
                    "day": "Monday",
                    "meals": [
                        {
                            "name": "Meal name",
                            "calories": 0,
                            "protein_g": 0,
                            "carbs_g": 0,
                            "fats_g": 0,
                        }
                    ],
                    "total_calories": 0,
                }
            ]
        },
        "rules": [
            "Return exactly 7 days",
            "Respect allergies strictly",
            "Ensure total calories per day approximately matches target",
            "Return valid JSON only",
        ],
    }