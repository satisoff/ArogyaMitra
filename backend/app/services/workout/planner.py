from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.planner import generate_ai_workout_outline
from app.services.workout.adaptive_engine import adapt_workout_plan
from app.services.tools.youtube_tool import search_youtube_video

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
        "exercises": _exercise_library(focus),
        "blocks": [
            {"name": "Warm-up", "minutes": warmup},
            {"name": "Main Session", "minutes": main_session},
            {"name": "Cool-down", "minutes": cooldown},
        ],
    }


def _duration_from_intensity(intensity: str, profile) -> int:
    base = profile.available_minutes_per_day or 15

    mapping = {
        "low": int(base * 0.6),
        "moderate": base,
        "high": int(base * 1.2),
    }

    return max(10, mapping.get(intensity, base))


def _exercise_from_notes(notes: str | None) -> list[str]:
    if not notes:
        return ["Bodyweight Squats", "Push-Ups", "Plank"]

    notes_lower = notes.lower()

    exercises = []

    if "push" in notes_lower:
        exercises.append("Push-Ups")
    if "plank" in notes_lower:
        exercises.append("Plank")
    if "squat" in notes_lower:
        exercises.append("Bodyweight Squats")
    if "curl" in notes_lower:
        exercises.append("Bicep Curls")
    if "press" in notes_lower:
        exercises.append("Shoulder Press")

    return exercises or ["Bodyweight Squats", "Push-Ups", "Plank"]


def _build_blocks(duration: int) -> list[dict]:
    warmup = 5
    cooldown = 5
    main = max(5, duration - warmup - cooldown)

    return [
        {"name": "Warm-up", "minutes": warmup},
        {"name": "Main Session", "minutes": main},
        {"name": "Cool-down", "minutes": cooldown},
    ]

def generate_workout_plan(
    user: User,
    profile: HealthProfile,
    context_flags: dict | None = None,
) -> dict:
    """
    Generate and adapt a structured 7-day workout plan.
    AI outline is primary driver.
    Deterministic planner is fallback.
    """

    ai_outline = generate_ai_workout_outline(
        user=user,
        profile=profile,
        extra_context=context_flags,
    )

    workout_days = []

    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    ai_days = ai_outline.get("days") if ai_outline else None

    for idx, day_name in enumerate(week_days):

        ai_day = ai_days[idx] if ai_days and idx < len(ai_days) else None

        if ai_day:
            # ---- AI-driven path ----

            focus = ai_day.get("focus", "General Training")

            intensity = ai_day.get("intensity", "low")
            if intensity not in ["low", "moderate", "high"]:
                intensity = "low"

            duration = _duration_from_intensity(intensity, profile)

            exercises = _exercise_from_notes(ai_day.get("notes"))

            blocks = _build_blocks(duration)

            workout_days.append({
                "day": day_name,
                "focus": focus,
                "location": profile.workout_location,
                "duration_minutes": duration,
                "exercises": exercises,
                "blocks": blocks,
            })

        else:
            # ---- Deterministic fallback ----
            fallback_day = _workout_for_day(
                idx,
                profile.workout_location,
                profile.available_minutes_per_day,
            )

            workout_days.append({
                "day": day_name,
                **fallback_day,
            })

    base_plan = {
        "user_id": user.id,
        "goal": user.fitness_goal or "general_fitness",
        "activity_level": profile.activity_level,
        "workout_location": profile.workout_location,
        "days": workout_days,
        "ai_outline": ai_outline,
    }

    return adapt_workout_plan(
        base_plan=base_plan,
        profile=profile,
        context_flags=context_flags,
    )