from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.time_capsule import TimeCapsule
from app.schemas.time_capsule import TimeCapsuleCreate, TimeCapsuleResponse

router = APIRouter()


@router.post("", response_model=TimeCapsuleResponse, status_code=status.HTTP_201_CREATED)
async def create_time_capsule(
    capsule_data: TimeCapsuleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """埋下时间胶囊"""
    # 验证投递时间必须是未来
    if capsule_data.deliver_at <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="投递时间必须是未来时间"
        )
    
    new_capsule = TimeCapsule(
        user_id=current_user.id,
        content=capsule_data.content,
        deliver_at=capsule_data.deliver_at
    )
    
    db.add(new_capsule)
    db.commit()
    db.refresh(new_capsule)
    
    return new_capsule


@router.get("/my", response_model=List[TimeCapsuleResponse])
async def get_my_time_capsules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取我的时间胶囊列表
    - 只返回已到投递时间的胶囊
    """
    now = datetime.utcnow()
    
    capsules = db.query(TimeCapsule).filter(
        TimeCapsule.user_id == current_user.id,
        TimeCapsule.deliver_at <= now
    ).all()
    
    # 标记为已投递
    for capsule in capsules:
        if not capsule.is_delivered:
            capsule.is_delivered = True
    
    db.commit()
    
    return capsules
