from typing import Type

import sqlalchemy

from db.repositories.base import BaseRepository
from db.tables.psychologist_specializations import Psychologist_specialization
from db.tables.psychologists import Psychologist
from models.psychologist import PsychologistIn, PsychologistOut


class PsychologistSpecializationsRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Psychologist_specialization

    @property
    def _schema_out(self) -> Type[PsychologistOut]:
        return PsychologistOut

    @property
    def _schema_in(self) -> Type[PsychologistIn]:
        return PsychologistIn

    async def list_with_specializations(self, specializations_ids: list, psychologist_repo: Psychologist):
        psychologists_ids = await self._db.fetch_all(query=self._table.select().where(
            self._table.c.specialization_id.in_(specializations_ids)).with_only_columns(
            [self._table.c.psychologist_id]))
        psychologists_ids = set([dict(p)['psychologist_id'] for p in psychologists_ids])
        rows = await self._db.fetch_all(query=psychologist_repo._table.select().where(
            psychologist_repo._table.c.id.in_(psychologists_ids)))
        return [psychologist_repo._schema_out(**dict(dict(row).items())) for row in rows] if rows else rows
