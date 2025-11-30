from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class PollCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    options: List[str] = Field(..., min_items=2, max_items=10)
    expires_at: Optional[datetime] = None


class PollVoteCreate(BaseModel):
    option_index: int


class PollResponse(BaseModel):
    id: int
    title: str
    options: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PollResultResponse(PollResponse):
    votes: List[int]  # 每个选项的票数
    total_votes: int
