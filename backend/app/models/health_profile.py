from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_level: Mapped[str] = mapped_column(String(50), nullable=False)
    workout_location: Mapped[str] = mapped_column(String(20), nullable=False)
    available_minutes_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    dietary_preference: Mapped[str] = mapped_column(String(100), nullable=False)
    injuries: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="health_profile")
