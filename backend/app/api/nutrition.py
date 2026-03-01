from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.nutrition import NutritionPlanResponse
from app.services.ai.nutrition_planner import generate_ai_nutrition_plan

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.post("/generate", response_model=NutritionPlanResponse)
def generate_nutrition(
    calorie_target: int,
    current_user: User = Depends(get_current_user),
):
    result = generate_ai_nutrition_plan(
        calorie_target=calorie_target,
        dietary_preference=current_user.fitness_goal or "balanced",
        allergies=current_user.allergies,
    )

    return {
        "user_id": current_user.id,
        "calorie_target": calorie_target,
        "dietary_preference": current_user.fitness_goal or "balanced",
        "allergies": current_user.allergies,
        "days": result.get("days", []),
        "source": result.get("source", "groq"),
    }