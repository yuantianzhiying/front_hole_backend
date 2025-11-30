from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.reaction import Reaction
from app.schemas.reaction import ReactionCreate, ReactionResponse

router = APIRouter()


@router.post("/{post_id}/reactions", response_model=ReactionResponse)
async def toggle_reaction(
    post_id: int,
    reaction_data: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    表态/点赞 (Toggle机制)
    - 如果已经点过，则取消
    - 如果没点过，则添加
    """
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    # 查找是否已经有该类型的表态
    existing_reaction = db.query(Reaction).filter(
        Reaction.post_id == post_id,
        Reaction.user_id == current_user.id,
        Reaction.reaction_type == reaction_data.type
    ).first()
    
    if existing_reaction:
        # 已存在，删除（取消表态）
        db.delete(existing_reaction)
        
        # 更新帖子点赞数（仅like类型）
        if reaction_data.type == "like":
            post.likes_count = max(0, post.likes_count - 1)
        
        db.commit()
        
        return ReactionResponse(
            message="表态已取消",
            action="removed"
        )
    else:
        # 不存在，添加
        new_reaction = Reaction(
            post_id=post_id,
            user_id=current_user.id,
            reaction_type=reaction_data.type
        )
        db.add(new_reaction)
        
        # 更新帖子点赞数（仅like类型）
        if reaction_data.type == "like":
            post.likes_count += 1
        
        db.commit()
        
        return ReactionResponse(
            message="表态成功",
            action="added"
        )
