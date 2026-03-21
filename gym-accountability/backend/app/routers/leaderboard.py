from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from uuid import UUID

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/global")
def global_leaderboard(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 5"})


@router.get("/group/{group_id}")
def group_leaderboard(group_id: UUID, _: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 5"})
