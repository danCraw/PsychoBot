from typing import Type, Union, Dict

import aioredis
import sqlalchemy
from aiogramBot.db.base import redis

from aiogramBot.db.repositories.base import BaseRepository
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

    async def set_temp_tariff(self, tg_id: int, tariff_name: str) -> _schema_out:
        await redis.set('tariff' + str(tg_id), tariff_name)

    async def set_temp_meets(self, tg_id: int, tariff_name: str) -> _schema_out:
        await redis.set('meets' + str(tg_id), tariff_name)

    async def have_tariff(self, tg_id: int) -> bool:
        client = await self.get(tg_id)
        return await redis.get('tariff' + str(tg_id)) or await redis.get(tg_id) or (client.tariff if client else None)
