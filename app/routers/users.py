from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas.user import UserPublic
from app.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import UserPublic, UserCreate
from app.db.models.user import User
from app.db.session import get_db
from app.core.security import get_password_hash
from app.dependencies import DBSessionDep, get_current_active_user

CurrentUserDep = Annotated[ AsyncSession, Depends(get_current_active_user)]

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={ 404: {"description": "Not found"}},
)

@router.get("/me", response_model=UserPublic)
async def current_user(current_user: CurrentUserDep):
    """
    Get the current active user.
    """
    return current_user

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: DBSessionDep):
    statement_user = select(User).where(User.username == user_in.username)
    result_user = await db.execute(statement_user)
    existing_user = result_user.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist")
    statement_email = select(User).where(User.email == user_in.email)
    result_email = await db.execute(statement_email)
    existing_email = result_email.scalars().first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user
