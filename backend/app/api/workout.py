from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.health_profile import HealthProfile
from app.models.user import User
from app.schemas.workout import WorkoutPlanResponse
from app.services.workout.planner import generate_workout_plan

router = APIRouter(prefix="/workout", tags=["Workout Planner"])


@router.post("/generate", response_model=WorkoutPlanResponse)
def generate_workout(
    travel: bool = Query(default=False),
    injury: bool = Query(default=False),
    low_time: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not found. Please create profile first.",
        )

    context_flags = {
        "travel": travel,
        "injury": injury,
        "low_time": low_time,
    }
    # print("Profile Injury Debug: ", profile.injuries);
    return generate_workout_plan(user=current_user, profile=profile, context_flags=context_flags)
