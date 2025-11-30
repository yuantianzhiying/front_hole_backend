from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    # 项目基础配置
    PROJECT_NAME: str = "校园树洞API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./treehole.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # CORS配置 - 使用字符串，支持逗号分隔
    ALLOWED_ORIGINS: str = "*"
    
    @property
    def cors_origins(self) -> List[str]:
        """将CORS配置转换为列表"""
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # 管理员配置
    ADMIN_TOKEN: str = "admin-secret-token-change-in-production"
    
    # 内容审核配置
    REPORT_THRESHOLD: int = 5  # 举报多少次自动隐藏
    
    # 敏感词列表
    SENSITIVE_WORDS: List[str] = [
        "自杀", "抑郁", "想死", "轻生", "结束生命",
        "政治敏感词1", "政治敏感词2"  # 根据实际需求添加
    ]
    
    # SOS关键词
    SOS_KEYWORDS: List[str] = ["自杀", "抑郁", "想死", "轻生", "结束生命"]
    
    # 随机昵称池
    NICKNAME_ADJECTIVES: List[str] = [
        "焦虑的", "快乐的", "迷茫的", "努力的", "佛系的",
        "积极的", "沉默的", "活泼的", "内向的", "外向的",
        "乐观的", "悲观的", "勇敢的", "害羞的", "自信的"
    ]
    
    NICKNAME_NOUNS: List[str] = [
        "高三党", "高一生", "高二生", "学霸", "学渣",
        "文科生", "理科生", "艺术生", "体育生", "社恐人",
        "夜猫子", "早起鸟", "追梦人", "打工人", "吃货"
    ]


settings = Settings()
