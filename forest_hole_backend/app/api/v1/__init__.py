from fastapi import APIRouter
from app.api.v1 import auth, posts, comments, reactions, reports, safety, bottles, time_capsules, polls, admin, utility

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(posts.router, prefix="/posts", tags=["帖子"])
api_router.include_router(comments.router, prefix="/posts", tags=["评论"])
api_router.include_router(reactions.router, prefix="/posts", tags=["表态"])
api_router.include_router(reports.router, prefix="/reports", tags=["举报"])
api_router.include_router(safety.router, prefix="/safety", tags=["安全检测"])
api_router.include_router(bottles.router, prefix="/bottles", tags=["漂流瓶"])
api_router.include_router(time_capsules.router, prefix="/time-capsules", tags=["时间胶囊"])
api_router.include_router(polls.router, prefix="/polls", tags=["投票"])
api_router.include_router(utility.router, prefix="/utility", tags=["实用工具"])
api_router.include_router(admin.router, prefix="/admin", tags=["管理后台"])
