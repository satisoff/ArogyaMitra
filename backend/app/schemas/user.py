from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    age: int | None = None
    fitness_goal: str | None = None
    allergies: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    age: int | None = None
    fitness_goal: str | None = None
    allergies: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
