from typing import Type, List

import sqlalchemy

from aiogramBot.db.repositories.base import BaseRepository
from aiogramBot.db.tables.meet import Meet
from aiogramBot.models.meet import MeetOut, MeetIn


class MeetRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Meet

    @property
    def _schema_out(self) -> Type[MeetOut]:
        return MeetOut

    @property
    def _schema_in(self) -> Type[MeetIn]:
        return MeetIn

    async def get_free_meets(self, day_of_the_week_id: int) -> List:
        rows = await self._db.fetch_all(query=self._table.select().where(self._table.c.day_of_the_week_id == day_of_the_week_id and self._table.c.client_id == None))
        return [self._schema_out(**dict(dict(row).items())) for row in rows]
