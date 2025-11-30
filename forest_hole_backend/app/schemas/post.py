from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    media_urls: Optional[List[str]] = []
    tag: Optional[str] = None
    nickname_style: Optional[str] = "random"


class PostResponse(BaseModel):
    id: int
    content: str
    media_urls: Optional[List[str]] = []
    tag: Optional[str]
    anonymous_nickname: str
    status: str
    likes_count: int
    comments_count: int
    has_sos_content: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    total: int
    page: int
    limit: int
    posts: List[PostResponse]


class PostDetailResponse(PostResponse):
    """帖子详情，包含评论"""
    comments: List["CommentResponse"] = []


# 避免循环导入
from app.schemas.comment import CommentResponse
PostDetailResponse.model_rebuild()
