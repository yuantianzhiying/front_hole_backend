from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.utils import generate_random_nickname, filter_sensitive_words
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter()


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    发表评论
    - 支持楼中楼回复
    - 自动标识楼主
    """
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    # 检查父评论是否存在（如果是楼中楼）
    if comment_data.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment_data.parent_id).first()
        if not parent_comment or parent_comment.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )
    
    # 过滤敏感词
    filtered_content = filter_sensitive_words(comment_data.content)
    
    # 生成匿名昵称
    nickname = generate_random_nickname()
    
    # 判断是否是楼主
    is_author = (current_user.id == post.user_id)
    
    # 创建评论
    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=filtered_content,
        parent_id=comment_data.parent_id,
        anonymous_nickname=nickname,
        is_author=is_author
    )
    
    db.add(new_comment)
    
    # 更新帖子评论数
    post.comments_count += 1
    
    db.commit()
    db.refresh(new_comment)
    
    return new_comment
