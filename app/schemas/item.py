# app/schemas/item.py
from pydantic import BaseModel, ConfigDict
from typing import List

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None

class ItemBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

    model_config = ConfigDict(from_attributes=True)

class ItemPublic(ItemBase):
    pass

class ItemList(BaseModel):
     items: List[ItemPublic]
