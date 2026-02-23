from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.planner import generate_ai_workout_outline
from app.services.workout.adaptive_engine import adapt_workout_plan


def _exercise_library(focus: str) -> list[str]:
    catalog = {
        "Full Body Strength": ["Barbell Squats", "Bench Press", "Cable Rows"],
        "Cardio + Core": ["Treadmill Intervals", "Mountain Climbers", "Plank Hold"],
        "Lower Body Strength": ["Deadlifts", "Leg Press", "Jump Squats"],
        "Mobility + Recovery": ["Hip Mobility Flow", "Thoracic Rotations", "Breathing Drills"],
        "Upper Body Strength": ["Bench Press", "Lat Pulldown", "Overhead Press"],
        "HIIT Conditioning": ["Burpees", "Sprint Intervals", "Box Jumps"],
        "Active Recovery Walk": ["Brisk Walk", "Gentle Stretching", "Foam Rolling"],
    }
    return catalog.get(focus, ["Bodyweight Squats", "Push-Ups", "Plank Hold"])


def _build_blocks(minutes: int) -> list[dict]:
    warmup = min(10, max(5, minutes // 6))
    cooldown = min(10, max(5, minutes // 8))
    main_session = max(10, minutes - warmup - cooldown)
    return [
        {"name": "Warm-up", "minutes": warmup},
        {"name": "Main Session", "minutes": main_session},
        {"name": "Cool-down", "minutes": cooldown},
    ]


def _normalize_intensity(intensity: str | None) -> str | None:
    if not intensity:
        return None
    value = intensity.strip().lower()
    if value in {"low", "moderate", "high"}:
        return value
    return None


def _is_valid_ai_days(ai_outline: dict) -> bool:
    days = ai_outline.get("days") if isinstance(ai_outline, dict) else None
    if not isinstance(days, list) or len(days) != 7:
        return False
    for day in days:
        if not isinstance(day, dict):
            return False
        if "focus" not in day:
            return False
    return True


def _duration_from_intensity(base_minutes: int, intensity: str | None) -> int:
    normalized = _normalize_intensity(intensity)
    if normalized == "high":
        return int(base_minutes * 1.1)
    if normalized == "low":
        return int(base_minutes * 0.85)
    return base_minutes


def _exercise_from_notes(focus: str, notes: str | None) -> list[str]:
    base_exercises = _exercise_library(focus)
    if not notes:
        return base_exercises

    text = notes.lower()
    if "mobility" in text or "recovery" in text:
        return ["Dynamic Stretching", "Hip Mobility Flow", "Breathing Drills"]
    if "core" in text:
        return ["Plank Hold", "Dead Bug", "Bird Dog"]
    if "interval" in text or "conditioning" in text:
        return ["Treadmill Intervals", "Air Bike", "Battle Ropes"]
    if "technique" in text or "form" in text:
        return ["Goblet Squats", "Incline Push-Ups", "Band Rows"]
    return base_exercises


def _workout_for_day(
    day_index: int,
    location: str,
    minutes: int,
    ai_day: dict | None = None,
) -> dict:
    templates = [
        "Full Body Strength",
        "Cardio + Core",
        "Lower Body Strength",
        "Mobility + Recovery",
        "Upper Body Strength",
        "HIIT Conditioning",
        "Active Recovery Walk",
    ]
    default_focus = templates[day_index % len(templates)]

    ai_focus = (ai_day or {}).get("focus")
    focus = ai_focus.strip() if isinstance(ai_focus, str) and ai_focus.strip() else default_focus

    ai_intensity = (ai_day or {}).get("intensity")
    final_minutes = _duration_from_intensity(minutes, ai_intensity)
    final_minutes = max(20, min(final_minutes, int(minutes * 1.2)))

    ai_notes = (ai_day or {}).get("notes")
    exercises = _exercise_from_notes(focus, ai_notes)

    return {
        "focus": focus,
        "location": location,
        "duration_minutes": final_minutes,
        "exercises": exercises,
        "blocks": _build_blocks(final_minutes),
    }


def generate_workout_plan(
    user: User,
    profile: HealthProfile,
    context_flags: dict | None = None,
) -> dict:
    """Generate and adapt a structured 7-day workout plan using modular mock logic."""
    ai_outline = generate_ai_workout_outline(user=user, profile=profile)
    ai_days = ai_outline.get("days", []) if _is_valid_ai_days(ai_outline) else []

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
        ai_day = ai_days[idx] if ai_days else None
        day_plan = _workout_for_day(
            idx,
            profile.workout_location,
            profile.available_minutes_per_day,
            ai_day=ai_day,
        )
        workout_days.append({"day": day_name, **day_plan})

    base_plan = {
        "user_id": user.id,
        "goal": user.fitness_goal or "general_fitness",
        "activity_level": profile.activity_level,
        "workout_location": profile.workout_location,
        "days": workout_days,
        "ai_outline": ai_outline,
    }
    return adapt_workout_plan(base_plan=base_plan, profile=profile, context_flags=context_flags)
