from pydantic import BaseModel


class WorkoutBlock(BaseModel):
    name: str
    minutes: int


class WorkoutDayPlan(BaseModel):
    day: str
    focus: str
    location: str
    duration_minutes: int
    exercises: list[str]
    blocks: list[WorkoutBlock]


class WorkoutAdaptations(BaseModel):
    travel_applied: bool
    injury_applied: bool
    low_time_applied: bool


class WorkoutPlanResponse(BaseModel):
    user_id: int
    goal: str
    activity_level: str
    workout_location: str
    days: list[WorkoutDayPlan]
    ai_outline: dict
    adaptations: WorkoutAdaptations
