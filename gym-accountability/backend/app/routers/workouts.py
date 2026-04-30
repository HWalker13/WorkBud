import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.reaction import Reaction
from app.models.user import User
from app.models.workout import Workout
from app.schemas.workout import WorkoutResponse, WorkoutSubmit
from app.services.ai_verify import verify_gym_photo
from app.services.s3 import generate_presigned_url

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/upload-url")
def get_upload_url(
    file_extension: str,
    current_user: User = Depends(get_current_user),
):
    settings = get_settings()
    key = f"workouts/{current_user.id}/{uuid.uuid4()}.{file_extension}"
    upload_url = generate_presigned_url(settings.aws_s3_bucket, key)
    return {"upload_url": upload_url, "s3_key": key}


@router.post("/", response_model=WorkoutResponse)
def submit_workout(
    body: WorkoutSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    image_url = (
        f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}"
        f".amazonaws.com/{body.s3_key}"
    )

    verified = verify_gym_photo(image_url)
    if not verified:
        raise HTTPException(
            status_code=400,
            detail="Photo could not be verified as a gym workout",
        )

    workout = Workout(
        user_id=current_user.id,
        photo_url=image_url,
        ai_verified=True,
        caption=body.caption,
        week_number=body.week_number,
        year=body.year,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


@router.get("/{workout_id}/reactions")
def get_reaction_counts(
    workout_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    upvotes = db.query(Reaction).filter(Reaction.workout_id == workout_id, Reaction.type == "upvote").count()
    tomatoes = db.query(Reaction).filter(Reaction.workout_id == workout_id, Reaction.type == "tomato").count()
    return {"upvotes": upvotes, "tomatoes": tomatoes}
