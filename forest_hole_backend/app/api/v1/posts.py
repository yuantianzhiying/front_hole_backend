from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import Optional
import json
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.utils import (
    generate_random_nickname, 
    check_sensitive_words, 
    filter_sensitive_words,
    check_sos_keywords,
    calculate_hot_score
)
from app.models.user import User
from app.models.post import Post, PostStatus
from app.schemas.post import PostCreate, PostResponse, PostListResponse, PostDetailResponse

router = APIRouter()


@router.get("", response_model=PostListResponse)
async def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("new", regex="^(new|hot)$"),
    tag: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取帖子列表
    - page: 页码
    - limit: 每页数量
    - sort: 排序方式 (new=最新, hot=热度)
    - tag: 标签筛选
    - keyword: 关键词搜索
    """
    query = db.query(Post).filter(Post.status == PostStatus.ACTIVE)
    
    # 标签筛选
    if tag:
        query = query.filter(Post.tag == tag)
    
    # 关键词搜索
    if keyword:
        query = query.filter(Post.content.contains(keyword))
    
    # 排序
    if sort == "hot":
        # 热度排序：需要计算热度分数
        posts = query.all()
        for post in posts:
            hours_ago = (datetime.utcnow() - post.created_at).total_seconds() / 3600
            post.hot_score = calculate_hot_score(
                post.likes_count, 
                post.comments_count, 
                hours_ago
            )
        posts.sort(key=lambda x: x.hot_score, reverse=True)
        
        # 分页
        total = len(posts)
        start = (page - 1) * limit
        end = start + limit
        posts = posts[start:end]
    else:
        # 时间排序
        total = query.count()
        posts = query.order_by(desc(Post.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    # 转换media_urls
    for post in posts:
        if post.media_urls:
            try:
                post.media_urls = json.loads(post.media_urls)
            except:
                post.media_urls = []
        else:
            post.media_urls = []
    
    return PostListResponse(
        total=total,
        page=page,
        limit=limit,
        posts=posts
    )


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    发布新帖子
    - 自动生成匿名昵称
    - 敏感词过滤
    - SOS关键词检测
    """
    # 敏感词检测
    has_sensitive, blocked_words = check_sensitive_words(post_data.content)
    if has_sensitive:
        # 过滤敏感词
        filtered_content = filter_sensitive_words(post_data.content)
    else:
        filtered_content = post_data.content
    
    # SOS关键词检测
    has_sos = check_sos_keywords(post_data.content)
    
    # 生成匿名昵称
    nickname = generate_random_nickname()
    
    # 创建帖子
    new_post = Post(
        user_id=current_user.id,
        content=filtered_content,
        media_urls=json.dumps(post_data.media_urls) if post_data.media_urls else None,
        tag=post_data.tag,
        anonymous_nickname=nickname,
        has_sos_content=has_sos,
        status=PostStatus.ACTIVE
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # 转换media_urls
    if new_post.media_urls:
        new_post.media_urls = json.loads(new_post.media_urls)
    else:
        new_post.media_urls = []
    
    return new_post


@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db)
):
    """获取帖子详情（包含评论）"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    if post.status == PostStatus.DELETED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子已被删除"
        )
    
    # 转换media_urls
    if post.media_urls:
        try:
            post.media_urls = json.loads(post.media_urls)
        except:
            post.media_urls = []
    else:
        post.media_urls = []
    
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除自己的帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    # 检查是否是帖子作者
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此帖子"
        )
    
    # 软删除
    post.status = PostStatus.DELETED
    db.commit()
    
    return {"message": "帖子已删除"}
