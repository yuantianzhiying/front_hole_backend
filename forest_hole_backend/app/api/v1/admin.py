from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime, timedelta
from typing import List

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.post import Post, PostStatus
from app.models.comment import Comment
from app.models.report import Report
from app.schemas.admin import DashboardResponse, AuditAction, AuditResponse
from app.schemas.post import PostResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    _: bool = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取仪表盘数据
    - 日活用户数
    - 今日发帖数
    - 待审核内容数
    - 总用户数
    - 总帖子数
    """
    # 今天的开始时间
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 日活用户数（今天发过帖或评论的用户）
    daily_active_users = db.query(func.count(func.distinct(Post.user_id))).filter(
        Post.created_at >= today_start
    ).scalar()
    
    # 今日发帖数
    daily_posts = db.query(func.count(Post.id)).filter(
        Post.created_at >= today_start
    ).scalar()
    
    # 待审核内容数（状态为pending或被举报超过阈值的）
    pending_audits = db.query(func.count(Post.id)).filter(
        or_(
            Post.status == PostStatus.PENDING,
            Post.status == PostStatus.HIDDEN
        )
    ).scalar()
    
    # 总用户数
    total_users = db.query(func.count(User.id)).scalar()
    
    # 总帖子数
    total_posts = db.query(func.count(Post.id)).scalar()
    
    return DashboardResponse(
        daily_active_users=daily_active_users or 0,
        daily_posts=daily_posts or 0,
        pending_audits=pending_audits or 0,
        total_users=total_users or 0,
        total_posts=total_posts or 0
    )


@router.get("/audit/list", response_model=List[PostResponse])
async def get_audit_list(
    status_filter: str = Query("pending", regex="^(pending|hidden|all)$"),
    _: bool = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取待审核内容列表
    - pending: 待审核
    - hidden: 被举报隐藏
    - all: 所有需要审核的
    """
    query = db.query(Post)
    
    if status_filter == "pending":
        query = query.filter(Post.status == PostStatus.PENDING)
    elif status_filter == "hidden":
        query = query.filter(Post.status == PostStatus.HIDDEN)
    else:  # all
        query = query.filter(
            or_(
                Post.status == PostStatus.PENDING,
                Post.status == PostStatus.HIDDEN
            )
        )
    
    posts = query.order_by(Post.created_at.desc()).all()
    
    # 转换media_urls
    import json
    for post in posts:
        if post.media_urls:
            try:
                post.media_urls = json.loads(post.media_urls)
            except:
                post.media_urls = []
        else:
            post.media_urls = []
    
    return posts


@router.put("/audit/{target_id}", response_model=AuditResponse)
async def audit_content(
    target_id: int,
    audit_data: AuditAction,
    _: bool = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    执行审核操作
    - approve: 通过审核
    - reject: 拒绝（删除）
    - ban_user: 封禁用户
    """
    # 获取目标内容
    if audit_data.target_type == "post":
        target = db.query(Post).filter(Post.id == target_id).first()
    else:  # comment
        target = db.query(Comment).filter(Comment.id == target_id).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{audit_data.target_type}不存在"
        )
    
    # 执行操作
    if audit_data.action == "approve":
        # 通过审核
        if audit_data.target_type == "post":
            target.status = PostStatus.ACTIVE
        message = "审核通过"
        
    elif audit_data.action == "reject":
        # 拒绝（删除）
        if audit_data.target_type == "post":
            target.status = PostStatus.DELETED
        else:
            db.delete(target)
        message = "内容已删除"
        
    elif audit_data.action == "ban_user":
        # 封禁用户
        user = db.query(User).filter(User.id == target.user_id).first()
        if user:
            user.is_banned = True
        
        # 同时删除内容
        if audit_data.target_type == "post":
            target.status = PostStatus.DELETED
        else:
            db.delete(target)
        
        message = "用户已封禁，内容已删除"
    
    db.commit()
    
    return AuditResponse(
        message=message,
        action=audit_data.action
    )


@router.get("/reports")
async def get_reports(
    _: bool = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """获取举报列表"""
    reports = db.query(Report).order_by(Report.created_at.desc()).limit(100).all()
    
    # 统计每个目标的举报次数
    report_stats = {}
    for report in reports:
        key = f"{report.target_type}_{report.target_id}"
        if key not in report_stats:
            report_stats[key] = {
                "target_type": report.target_type,
                "target_id": report.target_id,
                "count": 0,
                "reasons": []
            }
        report_stats[key]["count"] += 1
        report_stats[key]["reasons"].append(report.reason)
    
    return {
        "total": len(reports),
        "stats": list(report_stats.values())
    }
