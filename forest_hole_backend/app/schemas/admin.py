from pydantic import BaseModel
from typing import Literal


class DashboardResponse(BaseModel):
    daily_active_users: int
    daily_posts: int
    pending_audits: int
    total_users: int
    total_posts: int


class AuditAction(BaseModel):
    action: Literal["approve", "reject", "ban_user"]
    target_type: Literal["post", "comment"]


class AuditResponse(BaseModel):
    message: str
    action: str
