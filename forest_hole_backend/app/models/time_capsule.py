from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class TimeCapsule(Base):
    """时间胶囊模型"""
    __tablename__ = "time_capsules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    deliver_at = Column(DateTime(timezone=True), nullable=False, index=True)  # 投递时间
    is_delivered = Column(Boolean, default=False)  # 是否已投递
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
