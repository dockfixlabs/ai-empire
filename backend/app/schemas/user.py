from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    subscription_tier: str
    total_revenue: float
    total_products: int
    total_sales: int
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class GumroadConfig(BaseModel):
    gumroad_token: str
    gumroad_refresh_token: Optional[str] = None


class AIConfig(BaseModel):
    openai_api_key: Optional[str] = None
