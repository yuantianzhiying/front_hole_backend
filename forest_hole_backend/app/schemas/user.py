from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    device_id: Optional[str] = None
    openid: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    code: Optional[str] = None  # 微信登录code
    device_id: Optional[str] = None  # 设备指纹


class UserResponse(BaseModel):
    id: int
    is_banned: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
