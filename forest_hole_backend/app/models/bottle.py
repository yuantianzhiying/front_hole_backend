from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class Bottle(Base):
    """漂流瓶模型"""
    __tablename__ = "bottles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_picked = Column(Boolean, default=False)  # 是否已被捡起
    picked_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # 被谁捡起
    picked_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
