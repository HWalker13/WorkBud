from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/")
def submit_workout(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 2"})


@router.get("/")
def list_workouts(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 2"})
