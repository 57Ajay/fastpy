import redis.asyncio as redis
from app.core.config import settings

redis_pool = None

async def initialize_redis_pool():
    global redis_pool
    print(f"Starting redis pool with URL: {settings.REDIS_URL}")
    redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    try:
        async with redis.Redis(connection_pool=redis_pool,
            decode_responses=True,
        ) as redis_client:
            await redis_client.ping()
            print("Redis connection is alive.")
    except Exception as e:
        print(f"Redis connection error: {e}")
    
    return redis_pool

async def close_redis_pool():
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()


async def get_redis_client():
    """
    Get a Redis client from the pool.
    """
    global redis_pool
    if not redis_pool:
         raise Exception("Redis pool is not initialized.")
    client = redis.Redis.from_pool(redis_pool)
    print(f"Created Redis client: {client}")
    return client
