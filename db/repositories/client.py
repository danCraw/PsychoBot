from typing import Type, Union, Dict

import aioredis
import sqlalchemy

from core.base_config import config
from db.repositories.base import BaseRepository
from db.repositories.tariff import TariffRepository
from db.tables.client import Client
from models.base import BaseIdSchema, BaseSchema
from models.client import ClientOut, ClientIn, ClientBase
from redis_.base import redis_conn


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

    async def get(self, tg_id: str) -> _schema_out:
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
