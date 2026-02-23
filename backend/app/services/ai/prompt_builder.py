from app.models.health_profile import HealthProfile
from app.models.user import User


def build_workout_prompt(user: User, profile: HealthProfile) -> str:
    """Build a concise prompt for future AI-based workout planning."""
    return (
        "Create a 7-day workout plan for user with: "
        f"goal={user.fitness_goal or 'general_fitness'}, "
        f"age={user.age or 'not_specified'}, "
        f"activity_level={profile.activity_level}, "
        f"location={profile.workout_location}, "
        f"minutes_per_day={profile.available_minutes_per_day}, "
        f"injuries={profile.injuries or 'none'}."
    )
