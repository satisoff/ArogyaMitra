from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.workout import router as workout_router
from app.db.base import Base
from app.db.session import engine
from app.models import User  # noqa: F401 - ensure model registration

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ArogyaMitra AI Wellness API")
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(workout_router)


@app.get("/")
def root():
    return {"message": "ArogyaMitra backend running"}
