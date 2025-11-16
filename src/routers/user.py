from typing import Annotated
from fastapi import APIRouter, Query
# from fastapi.responses import JSONResponse
from src.models.user import User, SessionDep
from sqlmodel import select, Session

router = APIRouter(
    tags=["scg_requests"],
    responses={404: {"description": "Content not found"}},
)


@router.post("/users/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/all")
def read_users(
    session: SessionDep, offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
