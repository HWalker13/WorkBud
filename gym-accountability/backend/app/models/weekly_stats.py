import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class WeeklyStat(Base):
    __tablename__ = "weekly_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    goal = Column(Integer, nullable=False)
    completed = Column(Integer, nullable=False, default=0)
    streak_weeks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="weekly_stats")

    def __repr__(self) -> str:
        return f"<WeeklyStat user_id={self.user_id} week={self.week_number}/{self.year}>"
