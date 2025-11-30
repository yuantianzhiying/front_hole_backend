from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.poll import Poll, PollVote
from app.schemas.poll import PollCreate, PollVoteCreate, PollResponse, PollResultResponse

router = APIRouter()


@router.post("", response_model=PollResponse, status_code=status.HTTP_201_CREATED)
async def create_poll(
    poll_data: PollCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建投票"""
    new_poll = Poll(
        title=poll_data.title,
        options=json.dumps(poll_data.options, ensure_ascii=False),
        created_by=current_user.id,
        expires_at=poll_data.expires_at
    )
    
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)
    
    # 转换options
    new_poll.options = json.loads(new_poll.options)
    
    return new_poll


@router.get("/{poll_id}", response_model=PollResultResponse)
async def get_poll_result(
    poll_id: int,
    db: Session = Depends(get_db)
):
    """获取投票结果"""
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="投票不存在"
        )
    
    # 解析选项
    options = json.loads(poll.options)
    
    # 统计每个选项的票数
    votes = [0] * len(options)
    vote_records = db.query(PollVote).filter(PollVote.poll_id == poll_id).all()
    
    for vote in vote_records:
        if 0 <= vote.option_index < len(votes):
            votes[vote.option_index] += 1
    
    return PollResultResponse(
        id=poll.id,
        title=poll.title,
        options=options,
        created_at=poll.created_at,
        expires_at=poll.expires_at,
        votes=votes,
        total_votes=sum(votes)
    )


@router.post("/{poll_id}/vote")
async def vote_poll(
    poll_id: int,
    vote_data: PollVoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """参与投票"""
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="投票不存在"
        )
    
    # 验证选项索引
    options = json.loads(poll.options)
    if vote_data.option_index < 0 or vote_data.option_index >= len(options):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的选项索引"
        )
    
    # 创建投票记录
    new_vote = PollVote(
        poll_id=poll_id,
        user_id=current_user.id,
        option_index=vote_data.option_index
    )
    
    try:
        db.add(new_vote)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已经投过票了"
        )
    
    return {"message": "投票成功"}
