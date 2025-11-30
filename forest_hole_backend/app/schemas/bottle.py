from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BottleCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class BottleResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
