import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    photo_url = Column(String, nullable=False)
    ai_verified = Column(Boolean, nullable=False, default=False)
    ai_confidence_score = Column(Float, nullable=True)
    caption = Column(Text, nullable=True)
    week_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="workouts")
    reactions = relationship("Reaction", back_populates="workout", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Workout id={self.id} user_id={self.user_id} week={self.week_number}/{self.year}>"
