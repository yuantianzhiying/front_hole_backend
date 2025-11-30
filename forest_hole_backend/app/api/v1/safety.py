from fastapi import APIRouter

from app.core.utils import check_sensitive_words, check_sos_keywords
from app.schemas.safety import SafetyCheckRequest, SafetyCheckResponse

router = APIRouter()


@router.post("/check-text", response_model=SafetyCheckResponse)
async def check_text_safety(request: SafetyCheckRequest):
    """
    文本安全检测
    - 检测敏感词
    - 检测SOS关键词
    """
    has_sensitive, blocked_words = check_sensitive_words(request.content)
    has_sos = check_sos_keywords(request.content)
    
    if has_sensitive:
        message = "内容包含敏感词"
        pass_check = False
    elif has_sos:
        message = "检测到心理援助关键词，请注意用户心理健康"
        pass_check = True
    else:
        message = "内容安全"
        pass_check = True
    
    return SafetyCheckResponse(
        pass_check=pass_check,
        blocked_words=blocked_words,
        has_sos_content=has_sos,
        message=message
    )
