from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class PostStatus(str, enum.Enum):
    """帖子状态"""
    PENDING = "pending"  # 待审核
    ACTIVE = "active"    # 正常显示
    HIDDEN = "hidden"    # 被折叠/隐藏
    DELETED = "deleted"  # 已删除


class Post(Base):
    """帖子模型"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    media_urls = Column(Text, nullable=True)  # JSON字符串存储图片/音频URL列表
    tag = Column(String(50), index=True, nullable=True)  # 标签
    anonymous_nickname = Column(String(100), nullable=False)  # 匿名昵称
    status = Column(SQLEnum(PostStatus), default=PostStatus.ACTIVE, index=True)
    
    # 统计字段
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)
    
    # SOS标记
    has_sos_content = Column(Integer, default=0)  # 是否包含SOS关键词
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="post", cascade="all, delete-orphan")
