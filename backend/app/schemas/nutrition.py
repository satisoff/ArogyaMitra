from pydantic import BaseModel
from typing import List


class Meal(BaseModel):
    name: str
    calories: int
    protein_g: int
    carbs_g: int
    fats_g: int


class DailyMealPlan(BaseModel):
    day: str
    meals: List[Meal]
    total_calories: int


class NutritionPlanResponse(BaseModel):
    user_id: int
    calorie_target: int
    dietary_preference: str
    allergies: str | None
    days: List[DailyMealPlan]
    source: str