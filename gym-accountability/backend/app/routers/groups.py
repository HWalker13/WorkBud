from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/")
def list_groups(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 3"})


@router.post("/")
def create_group(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 3"})


@router.post("/join/{invite_code}")
def join_group(invite_code: str, _: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 3"})
