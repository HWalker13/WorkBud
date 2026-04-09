from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkoutCreate(BaseModel):
    photo_url: str
    caption: str | None = None
    week_number: int
    year: int


class WorkoutSubmit(BaseModel):
    s3_key: str
    caption: str | None = None
    week_number: int
    year: int


class WorkoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    photo_url: str
    ai_verified: bool
    ai_confidence_score: float | None
    caption: str | None
    week_number: int
    year: int
    created_at: datetime
