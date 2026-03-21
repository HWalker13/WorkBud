from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reactions", tags=["reactions"])


@router.post("/")
def add_reaction(_: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 3"})


@router.delete("/{reaction_id}")
def delete_reaction(reaction_id: UUID, _: User = Depends(get_current_user)):
    return JSONResponse(status_code=501, content={"detail": "Not implemented — Phase 3"})
