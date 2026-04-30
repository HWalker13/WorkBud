from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GroupCreate(BaseModel):
    name: str


class JoinGroup(BaseModel):
    invite_code: str


class GroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    invite_code: str
    created_by: UUID | None
    created_at: datetime
    member_count: int


class GroupMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    group_id: UUID
    user_id: UUID
    joined_at: datetime
