import json
from typing import Type, Union, Dict

import aioredis
import sqlalchemy
from aiogramBot.core.config import config

from aiogramBot.db.base import redis_conn
from aiogramBot.db.repositories.base import BaseRepository
from aiogramBot.db.repositories.tariff import TariffRepository
from aiogramBot.db.tables.client import Client
from aiogramBot.models.base import BaseIdSchema, BaseSchema
from aiogramBot.models.client import ClientOut, ClientIn, ClientBase


class ClientRepository(BaseRepository):
    def __init__(self, redis: aioredis.Redis = redis_conn, *args, **kwargs):
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

    async def create(self, values: Union[BaseSchema, Dict]) -> _schema_out:
        if isinstance(values, dict):
            values = self._schema_in(**values)
        dict_values = dict(values)

        await self._db.execute(query=self._table.insert(), values=dict_values)
        return self._schema_out(**dict_values)

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
            await self._db.execute(query=self._table.update().where(self._table.c.tg_id == dict_values['tg_id']),
                                   values=dict_values)
            return self._schema_out(**dict_values)
        return row

    async def get_temp_meets(self, tg_id: int):
        return await redis_conn.lrange('meets_' + str(tg_id), 1, -1)

    async def get_temp_tariff_id(self, tg_id: int):
        return await redis_conn.get('tariff_' + str(tg_id))

    async def get_temp_psychologist(self, tg_id):
        return await redis_conn.get('psychologist_' + str(tg_id))

    async def set_temp_tariff(self, tg_id: int, tariff_name: str) -> None:
        await redis_conn.set('tariff_' + str(tg_id), tariff_name, ex=config.EXPIRE_TIME)

    async def set_temp_meets(self, tg_id: int, meet_id: int) -> None:
        meets = await redis_conn.lrange('meets_' + str(tg_id), 1, -1)
        if not meets:
            while not meets:
                await redis_conn.rpush('meets_' + str(tg_id), meet_id, ex=config.EXPIRE_TIME)
                meets = await redis_conn.lrange('meets_' + str(tg_id), 1, -1, ex=config.EXPIRE_TIME)
                await redis_conn.rpush('selected_meets', meet_id, ex=config.EXPIRE_TIME)
        else:
            await redis_conn.rpush('meets_' + str(tg_id), meet_id, ex=config.EXPIRE_TIME)
            await redis_conn.rpush('selected_meets', meet_id, ex=config.EXPIRE_TIME)

    async def set_temp_psychologist(self, tg_id, psychologist_link: str):
        await redis_conn.set('psychologist_' + str(tg_id), psychologist_link, ex=config.EXPIRE_TIME)

    async def have_temp_tariff(self, tg_id: int) -> bool:
        return await redis_conn.get('tariff_' + str(tg_id))

    async def have_temp_meets(self, tg_id: int) -> bool:
        return await redis_conn.lrange('meets_' + str(tg_id), 1, -1)

    async def have_enough_meets(self, tg_id: int) -> bool:
        meets = await redis_conn.lrange('meets_' + str(tg_id), 1, -1)
        client_tariff_id = await redis_conn.get('tariff_' + str(tg_id))
        tariffs_repo: TariffRepository = TariffRepository()
        client_tariff = await tariffs_repo.get(client_tariff_id)
        return len(meets) == client_tariff.meets if meets else False

    async def delete_temp_data(self, tg_id: int):
        await redis_conn.delete('meets_' + str(tg_id))
        await redis_conn.delete('tariff_' + str(tg_id))
        await redis_conn.delete('selected_meets')

    async def delete_temp_meets(self, tg_id: int):
        await redis_conn.delete('meets_' + str(tg_id))

    async def save_temp_data_to_db(self, tg_id: int, username: str):
        meets = await redis_conn.lrange('meets_' + str(tg_id), 1, -1)
        client_tariff_id = await redis_conn.get('tariff_' + str(tg_id))
        if not client_tariff_id:
            return 422
        await self.create(ClientBase(tg_id=tg_id, name=username, tariff_id=client_tariff_id, remaining_meets=len(meets)))
        await self.delete_temp_data(tg_id)
