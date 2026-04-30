from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.reaction import Reaction
from app.models.user import User
from app.models.workout import Workout
from app.schemas.reaction import ReactionCreate, ReactionResponse

router = APIRouter(prefix="/reactions", tags=["reactions"])


@router.post("/", response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
def add_reaction(
    body: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout = db.query(Workout).filter(Workout.id == body.workout_id).first()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")

    if workout.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot react to your own workout")

    existing = (
        db.query(Reaction)
        .filter(Reaction.workout_id == body.workout_id, Reaction.user_id == current_user.id)
        .first()
    )

    if existing:
        existing.type = body.type.value
        db.commit()
        db.refresh(existing)
        return existing

    reaction = Reaction(workout_id=body.workout_id, user_id=current_user.id, type=body.type.value)
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction


@router.delete("/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reaction(
    reaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reaction = db.query(Reaction).filter(Reaction.id == reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found")

    if reaction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete another user's reaction")

    db.delete(reaction)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
