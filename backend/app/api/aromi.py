from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.health_profile import HealthProfile
from app.models.user import User
from app.services.ai.chat_agent import generate_aromi_response

router = APIRouter(prefix="/aromi", tags=["AROMI Coach"])


@router.post("/chat")
def aromi_chat(
    message: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == current_user.id).first()

    return generate_aromi_response(current_user, profile, message)