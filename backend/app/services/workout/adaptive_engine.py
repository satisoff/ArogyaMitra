from app.models.health_profile import HealthProfile


GYM_TO_BODYWEIGHT = {
    "Barbell Squats": "Air Squats",
    "Leg Press": "Walking Lunges",
    "Bench Press": "Push-Ups",
    "Lat Pulldown": "Resistance Band Rows",
    "Deadlifts": "Hip Hinge Good-Mornings",
    "Cable Rows": "Inverted Rows",
    "Treadmill Intervals": "Brisk Outdoor Walk",
    "Stationary Bike Sprints": "High-Knee Marches",
}

HIGH_IMPACT_EXERCISES = {
    "Box Jumps",
    "Burpees",
    "Jump Squats",
    "Sprint Intervals",
    "Mountain Climbers",
}

LOW_IMPACT_ALTERNATIVES = {
    "Box Jumps": "Step-Ups",
    "Burpees": "Walk-Outs",
    "Jump Squats": "Tempo Bodyweight Squats",
    "Sprint Intervals": "Power Walking Intervals",
    "Mountain Climbers": "Slow Knee Drives",
}


def _adapt_exercise_for_travel(exercise: str) -> str:
    return GYM_TO_BODYWEIGHT.get(exercise, exercise)


def _adapt_exercise_for_injury(exercise: str) -> str:
    if exercise in HIGH_IMPACT_EXERCISES:
        return LOW_IMPACT_ALTERNATIVES.get(exercise, "Low-Impact Mobility")
    return exercise


def _compress_blocks(day: dict, target_minutes: int) -> dict:
    blocks = day.get("blocks", [])
    if not blocks:
        day["duration_minutes"] = target_minutes
        return day

    planned_minutes = sum(block.get("minutes", 0) for block in blocks)
    if planned_minutes <= 0 or planned_minutes <= target_minutes:
        day["duration_minutes"] = min(day.get("duration_minutes", planned_minutes), target_minutes)
        return day

    ratio = target_minutes / planned_minutes
    new_minutes = [max(3, int(block.get("minutes", 0) * ratio)) for block in blocks]

    current_total = sum(new_minutes)
    idx = 0
    while current_total > target_minutes and idx < len(new_minutes):
        if new_minutes[idx] > 3:
            new_minutes[idx] -= 1
            current_total -= 1
        else:
            idx += 1
    idx = 0
    while current_total < target_minutes and new_minutes:
        new_minutes[idx % len(new_minutes)] += 1
        current_total += 1
        idx += 1

    for block, minutes in zip(blocks, new_minutes):
        block["minutes"] = minutes

    day["duration_minutes"] = target_minutes
    return day


def adapt_workout_plan(
    base_plan: dict,
    profile: HealthProfile,
    context_flags: dict | None = None,
) -> dict:
    """Apply adaptive workout rules for location, injuries and available time."""
    flags = context_flags or {}
    travel_mode = flags.get("travel", False) or profile.workout_location.lower() == "travel"
    injury_mode = flags.get("injury", False) or bool(profile.injuries and profile.injuries.strip())
    low_time_mode = flags.get("low_time", False) or any(
        day.get("duration_minutes", 0) > profile.available_minutes_per_day
        for day in base_plan.get("days", [])
    )

    for day in base_plan.get("days", []):
        exercises = day.get("exercises", [])
        updated_exercises = []

        for exercise in exercises:
            updated = exercise
            if travel_mode:
                updated = _adapt_exercise_for_travel(updated)
            if injury_mode:
                updated = _adapt_exercise_for_injury(updated)
            updated_exercises.append(updated)

        day["exercises"] = updated_exercises

        if low_time_mode and day.get("duration_minutes", 0) > profile.available_minutes_per_day:
            _compress_blocks(day, profile.available_minutes_per_day)

    base_plan["adaptations"] = {
        "travel_applied": travel_mode,
        "injury_applied": injury_mode,
        "low_time_applied": low_time_mode,
    }
    return base_plan
