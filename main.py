from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items, auth, users, notifications
from app.core.config import settings
from app.db.session import engine, Base
from contextlib import asynccontextmanager
from app.core.redis_pool import initialize_redis_pool, close_redis_pool
async def create_db_and_tables():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting up...")
    await initialize_redis_pool()
    yield
    print("Shutting down...")
    await engine.dispose()
    await close_redis_pool()
   
app = FastAPI(
    title="My Learning FastAPI App",
    description="An API built during the learning process.",
    version="0.1.0",
    lifespan=lifespan,
)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notifications.router)
@app.get("/")
async def read_root():
    print("Root endpoint accessed", settings)
    return {"name": "AJay Upadhyay, The king", "settings": settings}
