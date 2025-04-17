from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    def __repr__(self):
        """Return a string representation of the User object."""
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active})"
