from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """用户模型 - 存储真实身份信息"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # 用户名
    password_hash = Column(String, nullable=False)  # 密码哈希
    device_id = Column(String, unique=True, index=True, nullable=True)  # 设备指纹
    is_banned = Column(Boolean, default=False)  # 是否被封禁
    is_admin = Column(Boolean, default=False)  # 是否是管理员
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
