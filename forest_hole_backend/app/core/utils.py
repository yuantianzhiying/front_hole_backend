import random
import re
from typing import List, Tuple
from app.core.config import settings


def generate_random_nickname() -> str:
    """生成随机匿名昵称"""
    adjective = random.choice(settings.NICKNAME_ADJECTIVES)
    noun = random.choice(settings.NICKNAME_NOUNS)
    return f"{adjective}{noun}"


def check_sensitive_words(content: str) -> Tuple[bool, List[str]]:
    """
    检查敏感词
    返回: (是否包含敏感词, 命中的敏感词列表)
    """
    found_words = []
    for word in settings.SENSITIVE_WORDS:
        if word in content:
            found_words.append(word)
    
    return len(found_words) > 0, found_words


def filter_sensitive_words(content: str) -> str:
    """过滤敏感词，用*替换"""
    filtered_content = content
    for word in settings.SENSITIVE_WORDS:
        if word in filtered_content:
            filtered_content = filtered_content.replace(word, "*" * len(word))
    return filtered_content


def check_sos_keywords(content: str) -> bool:
    """检查是否包含SOS关键词（自杀/抑郁等）"""
    for keyword in settings.SOS_KEYWORDS:
        if keyword in content:
            return True
    return False


def calculate_hot_score(likes: int, comments: int, created_hours_ago: float) -> float:
    """
    计算热度分数
    公式: (点赞数 * 2 + 评论数 * 3) / (时间差 + 2)^1.5
    """
    interaction_score = likes * 2 + comments * 3
    time_decay = pow(created_hours_ago + 2, 1.5)
    return interaction_score / time_decay


def validate_tag(tag: str) -> bool:
    """验证标签是否有效"""
    valid_tags = ["crush", "rant", "help", "confession", "study", "life", "other"]
    return tag in valid_tags
