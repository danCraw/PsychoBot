from typing import Type, List

import sqlalchemy
from asyncpg import Record

from db.repositories.base import BaseRepository
from db.tables.tariff import Tariff
from models.tariff import TariffOut, TariffIn


class TariffRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Tariff

    @property
    def _schema_out(self) -> Type[TariffOut]:
        return TariffOut

    @property
    def _schema_in(self) -> Type[TariffIn]:
        return TariffIn

    async def _list(self) -> List[Record]:
        query = self._table.select().order_by(self._table.c.meets)
        return await self._db.fetch_all(query=query)

    async def get(self, tariff_name: str) -> _schema_out:
        row = await self._db.fetch_one(query=self._table.select().where(self._table.c.name == tariff_name))
        if row:
            return self._schema_out(**dict(dict(row).items()))
        else:
            return row
