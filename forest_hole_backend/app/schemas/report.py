from pydantic import BaseModel
from typing import Literal, Optional


class ReportCreate(BaseModel):
    target_type: Literal["post", "comment"]
    target_id: int
    reason: Literal["attack", "privacy", "fake", "spam", "other"]
    description: Optional[str] = None


class ReportResponse(BaseModel):
    message: str
    reports_count: int
