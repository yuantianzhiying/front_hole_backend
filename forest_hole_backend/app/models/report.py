from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Report(Base):
    """举报模型"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_type = Column(String(20), nullable=False)  # post 或 comment
    target_id = Column(Integer, nullable=False)
    reason = Column(String(50), nullable=False)  # attack, privacy, fake, etc.
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
