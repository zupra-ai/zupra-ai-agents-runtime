
import redis
from app.settings import settings
# Connect to Redis
redis_client = redis.Redis(host=settings.redis_host, port=int(settings.redis_port), decode_responses=True)