from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.core.database import Base


class Poll(Base):
    """投票模型"""
    __tablename__ = "polls"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    options = Column(Text, nullable=False)  # JSON字符串存储选项列表
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)


class PollVote(Base):
    """投票记录模型"""
    __tablename__ = "poll_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    option_index = Column(Integer, nullable=False)  # 选择的选项索引
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 唯一约束：一个用户对一个投票只能投一次
    __table_args__ = (
        UniqueConstraint('poll_id', 'user_id', name='unique_vote'),
    )
