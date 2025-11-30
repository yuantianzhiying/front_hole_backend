from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/daily-info")
async def get_daily_info():
    """
    获取每日信息
    - 倒计时（高考等重要日期）
    - 每日话题
    """
    # 计算高考倒计时（假设高考日期是每年6月7日）
    now = datetime.now()
    current_year = now.year
    gaokao_date = datetime(current_year, 6, 7)
    
    # 如果今年高考已过，计算到明年
    if now > gaokao_date:
        gaokao_date = datetime(current_year + 1, 6, 7)
    
    days_to_gaokao = (gaokao_date - now).days
    
    # 每日话题（可以从数据库读取，这里简化处理）
    daily_topics = [
        "今天最尴尬的事",
        "你最想对高三的自己说什么",
        "分享一个你的小确幸",
        "如果可以重来，你会改变什么",
        "说说你的梦想",
        "今天遇到的温暖瞬间",
        "你最喜欢的一句话"
    ]
    
    # 根据日期选择话题
    topic_index = now.timetuple().tm_yday % len(daily_topics)
    
    return {
        "countdown": {
            "event": "高考",
            "days": days_to_gaokao,
            "date": gaokao_date.strftime("%Y-%m-%d")
        },
        "daily_topic": {
            "title": daily_topics[topic_index],
            "id": topic_index + 1
        }
    }
