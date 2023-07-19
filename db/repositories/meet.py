from typing import Type, List

import sqlalchemy

from redis_.base import redis_conn
from db.repositories.base import BaseRepository
from db.tables.meet import Meet
from models.meet import MeetOut, MeetIn


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
        selected_meets = await redis_conn.lrange('selected_meets', 1, -1)
        rows = await self._db.fetch_all(query=self._table.select().where(self._table.c.day_of_the_week_id == day_of_the_week_id
                                                                         and self._table.c.client_id is None
                                                                         and self._table.c.id not in selected_meets))
        return [self._schema_out(**dict(dict(row).items())) for row in rows]
