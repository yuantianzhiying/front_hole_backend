from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    parent_id: Optional[int]
    anonymous_nickname: str
    is_author: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
