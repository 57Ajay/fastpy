from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from app.core.redis_pool import get_redis_client
from app.db.session import get_db
from app.db.models.user import User
from app.core.config import settings
from app.core.security import oauth2_scheme, TokenData

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSessionDep
) -> User:
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # Extract username from 'sub' claim
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception

        # (Optional) Validate payload structure using TokenData schema
        token_data = TokenData(username=username)

    except JWTError:
        # If token is invalid (bad signature, expired, etc.)
        raise credentials_exception

    # Fetch user from database based on username from token
    statement = select(User).where(User.username == token_data.username)
    result = await db.execute(statement)
    user = result.scalars().first()

    if user is None:
        # If user associated with token doesn't exist anymore
        raise credentials_exception

    # You could return a Pydantic schema here too (e.g., UserInDB),
    # but returning the DB model can be convenient for use in endpoints.
    return user

# Dependency for getting the current active user (optional refinement)
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency that relies on get_current_user but also checks if user is active.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_redis():
    return await get_redis_client()
