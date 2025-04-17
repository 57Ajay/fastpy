from sqlalchemy import Boolean, Integer, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tax: Mapped[float | None] = mapped_column(Float, default=None, nullable=True)

    # __repr__ (optional but helpful for debugging)
    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price})>"

