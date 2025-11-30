from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.bottle import Bottle
from app.schemas.bottle import BottleCreate, BottleResponse

router = APIRouter()


@router.post("", response_model=BottleResponse, status_code=status.HTTP_201_CREATED)
async def throw_bottle(
    bottle_data: BottleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """扔漂流瓶"""
    new_bottle = Bottle(
        user_id=current_user.id,
        content=bottle_data.content
    )
    
    db.add(new_bottle)
    db.commit()
    db.refresh(new_bottle)
    
    return new_bottle


@router.get("/draw", response_model=BottleResponse)
async def draw_bottle(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    捡漂流瓶
    - 随机返回一个未被捡起的漂流瓶
    - 不会捡到自己扔的瓶子
    """
    # 查找未被捡起且不是自己扔的瓶子
    bottle = db.query(Bottle).filter(
        Bottle.is_picked == False,
        Bottle.user_id != current_user.id
    ).order_by(func.random()).first()
    
    if not bottle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="暂时没有可捡的漂流瓶"
        )
    
    # 标记为已捡起
    bottle.is_picked = True
    bottle.picked_by = current_user.id
    bottle.picked_at = datetime.utcnow()
    
    db.commit()
    db.refresh(bottle)
    
    return bottle
