from typing import Type

import sqlalchemy
from sqlalchemy import func

from db.repositories.base import BaseRepository
from db.tables.psychologist_specializations import Psychologist_specialization
from db.tables.psychologists import Psychologist
from db.tables.specializations import Specialization
from models.psychologist import PsychologistIn, PsychologistOut


class PsychologistRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Psychologist

    @property
    def _schema_out(self) -> Type[PsychologistOut]:
        return PsychologistOut

    @property
    def _schema_in(self) -> Type[PsychologistIn]:
        return PsychologistIn

    async def approved_psychologists(self, limit: int, offset: int, specializations_table: Specialization, psychologists_specializations_table: Psychologist_specialization) -> list[PsychologistOut]:
        rows = await self._db.fetch_all(
                        self._table.select()
                            .join(psychologists_specializations_table,
                                  self._table.c.id == psychologists_specializations_table.c.psychologist_id,
                                  isouter=True)
                            .join(specializations_table,
                                  psychologists_specializations_table.c.specialization_id == specializations_table.c.id,
                                  isouter=True)
                            .where(self._table.c.approved == True)
                            .with_only_columns(
                                self._table.c.id,
                                self._table.c.name,
                                self._table.c.tg_link,
                                self._table.c.age,
                                self._table.c.description,
                                self._table.c.photo,
                                self._table.c.meet_price,
                                self._table.c.likes,
                                self._table.c.approved,
                                func.array_remove(func.array_agg(specializations_table.c.name), None).label('specializations')
                            )
                        .group_by(self._table.c.id)
                        .limit(limit)
                        .offset(offset)
                    )
        return [self._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows
