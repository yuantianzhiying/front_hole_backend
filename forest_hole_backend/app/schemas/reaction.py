from pydantic import BaseModel
from typing import Literal


class ReactionCreate(BaseModel):
    type: Literal["like", "hug", "popcorn", "plus1"]


class ReactionResponse(BaseModel):
    message: str
    action: str  # "added" or "removed"
