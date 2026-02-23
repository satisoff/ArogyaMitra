from pydantic import BaseModel, ConfigDict


class HealthProfileUpsert(BaseModel):
    height: int
    weight: int
    activity_level: str
    workout_location: str
    available_minutes_per_day: int
    dietary_preference: str
    injuries: str | None = None


class HealthProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    height: int
    weight: int
    activity_level: str
    workout_location: str
    available_minutes_per_day: int
    dietary_preference: str
    injuries: str | None = None
