from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReactionTypeEnum(str, Enum):
    upvote = "upvote"
    tomato = "tomato"


class ReactionCreate(BaseModel):
    workout_id: UUID
    type: ReactionTypeEnum


class ReactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workout_id: UUID
    user_id: UUID
    type: ReactionTypeEnum
    created_at: datetime
