from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.post import Post, PostStatus
from app.models.comment import Comment
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter()


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    提交举报
    - 当举报数超过阈值时自动隐藏内容
    """
    # 验证目标是否存在
    if report_data.target_type == "post":
        target = db.query(Post).filter(Post.id == report_data.target_id).first()
    else:  # comment
        target = db.query(Comment).filter(Comment.id == report_data.target_id).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{report_data.target_type}不存在"
        )
    
    # 创建举报记录
    new_report = Report(
        user_id=current_user.id,
        target_type=report_data.target_type,
        target_id=report_data.target_id,
        reason=report_data.reason,
        description=report_data.description
    )
    
    db.add(new_report)
    
    # 统计该目标的举报次数
    reports_count = db.query(Report).filter(
        Report.target_type == report_data.target_type,
        Report.target_id == report_data.target_id
    ).count() + 1
    
    # 如果是帖子，更新举报计数
    if report_data.target_type == "post":
        target.reports_count = reports_count
        
        # 超过阈值自动隐藏
        if reports_count >= settings.REPORT_THRESHOLD:
            target.status = PostStatus.HIDDEN
    
    db.commit()
    
    return ReportResponse(
        message="举报已提交",
        reports_count=reports_count
    )
