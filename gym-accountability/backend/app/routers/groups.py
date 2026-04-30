import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.group import Group, GroupMember
from app.models.user import User
from app.models.workout import Workout
from app.schemas.group import GroupCreate, GroupMemberResponse, GroupResponse, JoinGroup
from app.schemas.workout import WorkoutResponse

router = APIRouter(prefix="/groups", tags=["groups"])


def _build_response(group: Group) -> GroupResponse:
    return GroupResponse(
        id=group.id,
        name=group.name,
        invite_code=group.invite_code,
        created_by=group.created_by,
        created_at=group.created_at,
        member_count=len(group.members),
    )


def _assert_member(group_id: UUID, user_id, db: Session) -> None:
    membership = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    body: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    while True:
        invite_code = secrets.token_urlsafe(6)
        if not db.query(Group).filter(Group.invite_code == invite_code).first():
            break

    group = Group(name=body.name, invite_code=invite_code, created_by=current_user.id)
    db.add(group)
    db.flush()

    member = GroupMember(group_id=group.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    db.refresh(group)
    return _build_response(group)


@router.get("/", response_model=list[GroupResponse])
def list_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    memberships = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    groups = []
    for m in memberships:
        db.refresh(m.group)
        groups.append(_build_response(m.group))
    return groups


@router.post("/join", response_model=GroupResponse)
def join_group(
    body: JoinGroup,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    group = db.query(Group).filter(Group.invite_code == body.invite_code).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid invite code")

    already_member = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group.id, GroupMember.user_id == current_user.id)
        .first()
    )
    if already_member:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already a member of this group")

    member = GroupMember(group_id=group.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    db.refresh(group)
    return _build_response(group)


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
def list_members(
    group_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_member(group_id, current_user.id, db)
    return db.query(GroupMember).filter(GroupMember.group_id == group_id).all()


@router.get("/{group_id}/feed", response_model=list[WorkoutResponse])
def group_feed(
    group_id: UUID,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_member(group_id, current_user.id, db)

    member_ids = [
        m.user_id
        for m in db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    ]

    return (
        db.query(Workout)
        .filter(Workout.user_id.in_(member_ids))
        .order_by(Workout.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
