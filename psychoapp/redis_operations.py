import pickle

from psychoapp.all_constants import redis
from psychoapp.client_getters import get_client
from psychoapp.models import Client, Meet


def add_client_to_redis(client_id, client_name, client_tariff):
    redis.set(client_id, pickle.dumps(Client(client_id, client_name, client_tariff, 0)))


def get_client_from_redis(client_id) -> Client:
    try:
        return pickle.loads(redis.get(client_id))
    except Exception:
        print('client not exist')


def save_client_from_redis_to_db(client_id):
    client = get_client(client_id)
    Client.objects.create(tg_id=client.tg_id, name=client.name, tariff=client.tariff, remaining_meets=client.tariff.meets)
    print('client created')


def save_client_meets_from_redis_to_db(client_id):
    client_meets = redis.smembers(str(client_id)+'_meets')
    for m in client_meets:
        m = pickle.loads(m)
        meet_from_db = Meet.objects.get(id=m.id)
        meet_from_db.client = m.client
        meet_from_db.save()
