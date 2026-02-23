from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.health_profile import HealthProfile
from app.models.user import User
from app.schemas.health_profile import HealthProfileResponse, HealthProfileUpsert

router = APIRouter(tags=["Health Profile"])


@router.post("/profile", response_model=HealthProfileResponse)
def upsert_profile(
    profile_in: HealthProfileUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()

    if profile:
        profile.height = profile_in.height
        profile.weight = profile_in.weight
        profile.activity_level = profile_in.activity_level
        profile.workout_location = profile_in.workout_location
        profile.available_minutes_per_day = profile_in.available_minutes_per_day
        profile.dietary_preference = profile_in.dietary_preference
        profile.injuries = profile_in.injuries
    else:
        profile = HealthProfile(
            user_id=current_user.id,
            height=profile_in.height,
            weight=profile_in.weight,
            activity_level=profile_in.activity_level,
            workout_location=profile_in.workout_location,
            available_minutes_per_day=profile_in.available_minutes_per_day,
            dietary_preference=profile_in.dietary_preference,
            injuries=profile_in.injuries,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profile", response_model=HealthProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile
