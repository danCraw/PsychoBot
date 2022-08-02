import redis

redis = redis.StrictRedis(host='localhost', port=6379, db=1)

REDIS_TEMP_TIMEOUT = 900
