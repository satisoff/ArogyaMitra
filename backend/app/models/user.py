from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fitness_goal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)


    health_profile = relationship("HealthProfile", back_populates="user", uselist=False)
