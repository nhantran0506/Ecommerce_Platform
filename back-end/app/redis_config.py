from redis import Redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

def get_redis():
    try:
        redis_client.ping()
        return redis_client
    except Exception as e:
        raise Exception(f"Could not connect to Redis: {str(e)}") 