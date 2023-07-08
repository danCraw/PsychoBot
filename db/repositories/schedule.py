from typing import Type, Union, List

import sqlalchemy

from db.repositories.base import BaseRepository
from db.tables.schedule import Schedule
from models.schedule import ScheduleIn, ScheduleOut


class ScheduleRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Schedule

    @property
    def _schema_out(self) -> Type[ScheduleOut]:
        return ScheduleOut

    @property
    def _schema_in(self) -> Type[ScheduleIn]:
        return ScheduleIn

    async def get_psychologist_schedule(self, psychologist_id: Union[int, str]) -> List:
        rows = await self._db.fetch_all(query=self._table.select().where(self._table.c.psychologist_id == psychologist_id))
        return [self._schema_out(**dict(dict(row).items())) for row in rows]
