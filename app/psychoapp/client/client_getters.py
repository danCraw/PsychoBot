import pickle

from psychoapp.all_constants import redis
from psychoapp.models import Client


def get_amount_client_meets(client_id) -> int:
    meets = redis.smembers(str(client_id)+'_meets')
    if meets:
        return len(meets)
    else:
        return 0


def get_amount_client_tariff_meets(client_id) -> int:
    client = get_client(client_id)
    return client.tariff.meets


def get_client_psycho_tg_link(client_id: int):
    meets = redis.smembers(str(client_id) + '_meets')
    for m in meets:
        meet = pickle.loads(m)
    return meet.day_of_the_week.psychologist.tg_link


def get_client(client_id: int):
    client_from_redis = redis.get(client_id)
    if client_from_redis:
        return pickle.loads(client_from_redis)
    else:
        client_from_db = Client.objects.get(tg_id=client_id)
        if client_from_db:
            return client_from_db
        else:
            print('client not exist create again')