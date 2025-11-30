from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reaction(Base):
    """表态/点赞模型"""
    __tablename__ = "reactions"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reaction_type = Column(String(20), nullable=False)  # like, hug, popcorn, plus1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    post = relationship("Post", back_populates="reactions")
    
    # 唯一约束：一个用户对一个帖子的同一类型只能表态一次
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', 'reaction_type', name='unique_reaction'),
    )
