"""
Redis istemcisi (tekil). Oturum deposu ve menü önbelleği bunu paylaşır.
decode_responses=True: değerler str olarak okunur/yazılır.
"""
import redis

from ..config import ayar

istemci = redis.Redis(
    host=ayar.REDIS_HOST,
    port=ayar.REDIS_PORT,
    decode_responses=True,
)
