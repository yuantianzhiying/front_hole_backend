from pydantic import BaseModel, Field
from datetime import datetime


class TimeCapsuleCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    deliver_at: datetime


class TimeCapsuleResponse(BaseModel):
    id: int
    content: str
    deliver_at: datetime
    is_delivered: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
