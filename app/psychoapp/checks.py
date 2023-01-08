import pickle

from psychoapp.all_constants import redis
from psychoapp.models import Client


def client_already_have_this_meet(client_id, meet_id) -> bool:
    meets = redis.smembers((str(client_id) + '_meets'))
    try:
        for m in meets:
            if meet_id == pickle.loads(m).id:
                print('okkk')
                return True
        return False
    except Exception:
        return False


def client_exist(client_id: int):
    try:
        Client.objects.get(tg_id=client_id)
        return True
    except Exception:
        return False


def client_have_tariff(client_id) -> bool:
    try:
        if redis.get(client_id) or Client.objects.get(tg_id=client_id):
            return True
    except Exception as e:
        print(e)
    else:
        return False