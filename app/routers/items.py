from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Annotated
import redis.asyncio as redis
from app.dependencies import get_redis
from app.schemas.item import ItemPublic, ItemCreate, ItemUpdate
from app.db.session import get_db
from app.db.models.item import Item

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]
RedisDep = Annotated[redis.Redis, Depends(get_redis)]

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: DBSessionDep):
    """
    Create a new item in the database.
    """
    new_db_item = Item(**item.model_dump())
    db.add(new_db_item)
    await db.commit()
    await db.refresh(new_db_item)
    return new_db_item


@router.get("/", response_model=List[ItemPublic])
async def read_items(db: DBSessionDep, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of items from the database.
    """
    statement = select(Item).offset(skip).limit(limit)
    result = await db.execute(statement)
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=ItemPublic)
async def read_item(item_id: int, db: DBSessionDep, redis_client: RedisDep):
    """
    Retrieve a single item by its ID.
    """
    print(f"this is redis client: {redis_client}")
    cached_key = f"item_{item_id}"
    cached_item_data = await redis_client.get(cached_key)
    if cached_item_data:
        try:
            item = ItemPublic.model_validate_json(cached_item_data)
            return item
        except Exception as e:
            print(f"Error deserializing cached item data: {e}")
    db_item = await db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item_to_cache = ItemPublic.model_validate(db_item)
    print(f"Item to cache: {item_to_cache}")
    await redis_client.set(cached_key, item_to_cache.model_dump_json(), ex=300)
    return item_to_cache


@router.put("/{item_id}", response_model=ItemPublic)
async def update_item(item_id: int, item_update: ItemUpdate, db: DBSessionDep, redis_client: RedisDep):
    """
    Update an existing item by ID.
    """
    db_item = await db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    await redis_client.delete(f"item_{item_id}")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: DBSessionDep, redis_client: RedisDep):
    """
    Delete an item by ID.
    """
    db_item = await db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
    await redis_client.delete(f"item_{item_id}")
    return None
