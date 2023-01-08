from typing import Type

import sqlalchemy

from aiogramBot.db.repositories.base import BaseRepository
from aiogramBot.db.tables.psyhologist import Psychologist
from aiogramBot.models.psyhologists import PsychologistOut, PsychologistIn


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
