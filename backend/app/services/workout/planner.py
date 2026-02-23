from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.planner import generate_ai_workout_outline


def _workout_for_day(day_index: int, location: str, minutes: int) -> dict:
    templates = [
        "Full Body Strength",
        "Cardio + Core",
        "Lower Body Strength",
        "Mobility + Recovery",
        "Upper Body Strength",
        "HIIT Conditioning",
        "Active Recovery Walk",
    ]
    focus = templates[day_index % len(templates)]
    warmup = min(10, max(5, minutes // 6))
    cooldown = min(10, max(5, minutes // 8))
    main_session = max(10, minutes - warmup - cooldown)

    return {
        "focus": focus,
        "location": location,
        "duration_minutes": minutes,
        "blocks": [
            {"name": "Warm-up", "minutes": warmup},
            {"name": "Main Session", "minutes": main_session},
            {"name": "Cool-down", "minutes": cooldown},
        ],
    }


def generate_workout_plan(user: User, profile: HealthProfile) -> dict:
    """Generate a structured 7-day workout plan using mock logic for now."""
    ai_outline = generate_ai_workout_outline(user=user, profile=profile)

    workout_days = []
    for idx, day_name in enumerate(
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    ):
        day_plan = _workout_for_day(
            idx,
            profile.workout_location,
            profile.available_minutes_per_day,
        )
        workout_days.append({"day": day_name, **day_plan})

    return {
        "user_id": user.id,
        "goal": user.fitness_goal or "general_fitness",
        "activity_level": profile.activity_level,
        "workout_location": profile.workout_location,
        "days": workout_days,
        "ai_outline": ai_outline,
    }
