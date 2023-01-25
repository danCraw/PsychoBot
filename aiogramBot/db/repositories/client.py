import json
from typing import Type, Union, Dict

import aioredis
import sqlalchemy
from aiogramBot.core.config import config

from aiogramBot.db.base import redis
from aiogramBot.db.repositories.base import BaseRepository
from aiogramBot.db.repositories.tariff import TariffRepository
from aiogramBot.db.tables.client import Client
from aiogramBot.models.base import BaseIdSchema
from aiogramBot.models.client import ClientOut, ClientIn


class ClientRepository(BaseRepository):
    def __init__(self, redis: aioredis.Redis = redis, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _table(self) -> sqlalchemy.Table:
        return Client

    @property
    def _schema_out(self) -> Type[ClientOut]:
        return ClientOut

    @property
    def _schema_in(self) -> Type[ClientIn]:
        return ClientIn

    async def get(self, tg_id: int) -> _schema_out:
        row = await self._db.fetch_one(query=self._table.select().where(self._table.c.tg_id == tg_id))
        if row:
            return self._schema_out(**dict(dict(row).items()))
        else:
            return row

    async def update(self, values: Union[BaseIdSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = self._preprocess_create(dict(values))
        row = await self.get(dict_values['tg_id'])
        if row:
            await self._db.execute(query=self._table.update().where(self._table.c.id == dict_values['tg_id']),
                                   values=dict_values)
            return self._schema_out(**dict_values)
        return row

    async def get_temp_meets(self, tg_id: int):
        return await redis.lrange('meets_' + str(tg_id), 1, -1)

    async def get_temp_tariff_id(self, tg_id: int):
        return await redis.get('tariff_' + str(tg_id))

    async def set_temp_tariff(self, tg_id: int, tariff_name: str) -> None:
        await redis.set('tariff_' + str(tg_id), tariff_name)

    async def set_temp_meets(self, tg_id: int, meet_id: int) -> None:
        meets = await redis.lrange('meets_' + str(tg_id), 1, -1)
        if meets:
            await redis.rpush('meets_' + str(tg_id), meet_id, ex=config.EXPIRE_TIME)
        else:
            await redis.rpush('meets_' + str(tg_id), meet_id)

    async def have_temp_tariff(self, tg_id: int) -> bool:
        return await redis.get('tariff_' + str(tg_id))

    async def have_temp_meets(self, tg_id: int) -> bool:
        return await redis.get('meets_' + str(tg_id))

    async def have_enough_meets(self, tg_id: int) -> bool:
        meets = await redis.lrange('meets_' + str(tg_id), 1, -1)
        client_tariff_id = await redis.get('tariff_' + str(tg_id))
        tariffs_repo: TariffRepository = TariffRepository()
        client_tariff = await tariffs_repo.get(client_tariff_id)
        return len(meets) == client_tariff.meets if meets else False

    async def delete_temp_data(self, tg_id: int):
        await redis.delete('meets_' + str(tg_id))
        await redis.delete('tariff_' + str(tg_id))

    async def delete_temp_meets(self, tg_id: int):
        await redis.delete('meets_' + str(tg_id))

    async def save_temp_data_to_db(self, tg_id: int):
        meets = await redis.lrange('meets_' + str(tg_id), 1, -1)
        client_tariff_id = await redis.get('tariff_' + str(tg_id))
        self.update({'tariff_if': client_tariff_id, 'remaining_meets': len(meets)})
