from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserLogin, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录/注册
    - 支持微信小程序code登录
    - 支持设备指纹登录
    """
    user = None
    
    # 微信登录
    if user_data.code:
        # TODO: 调用微信API获取openid
        # 这里简化处理，实际需要调用微信接口
        openid = f"wx_{user_data.code}"
        
        user = db.query(User).filter(User.openid == openid).first()
        if not user:
            user = User(openid=openid)
            db.add(user)
            db.commit()
            db.refresh(user)
    
    # 设备指纹登录
    elif user_data.device_id:
        user = db.query(User).filter(User.device_id == user_data.device_id).first()
        if not user:
            user = User(device_id=user_data.device_id)
            db.add(user)
            db.commit()
            db.refresh(user)
    
    else:
        # 如果都没有，生成一个临时设备ID
        device_id = str(uuid.uuid4())
        user = User(device_id=device_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 检查是否被封禁
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被封禁"
        )
    
    # 生成JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "is_admin": user.is_admin}
    )
    
    return TokenResponse(access_token=access_token)
