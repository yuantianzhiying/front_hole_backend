from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """评论模型"""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # 楼中楼
    anonymous_nickname = Column(String(100), nullable=False)
    is_author = Column(Boolean, default=False)  # 是否是楼主
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])
