from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WeeklyStatCreate(BaseModel):
    week_number: int
    year: int
    goal: int


class WeeklyStatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    week_number: int
    year: int
    goal: int
    completed: int
    streak_weeks: int
    created_at: datetime
