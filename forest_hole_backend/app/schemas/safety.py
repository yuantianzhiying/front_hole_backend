from pydantic import BaseModel
from typing import List


class SafetyCheckRequest(BaseModel):
    content: str


class SafetyCheckResponse(BaseModel):
    pass_check: bool
    blocked_words: List[str]
    has_sos_content: bool
    message: str
