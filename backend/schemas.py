from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ReportCreate(BaseModel):
    topic: str = Field(min_length=2, max_length=500)
    max_results: int = Field(default=3, ge=1, le=5)


class ReportOut(BaseModel):
    id: int
    topic: str
    report: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReportGenerateOut(BaseModel):
    status: str
    report: ReportOut
