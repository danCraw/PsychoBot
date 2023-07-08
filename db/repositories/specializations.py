from typing import Type, Union, List

import sqlalchemy

from db.repositories.base import BaseRepository
from db.tables.specializations import Specialization
from models.specializations import SpecializationIn, SpecializationOut


class SpecializationRepository(BaseRepository):
    @property
    def _table(self) -> sqlalchemy.Table:
        return Specialization

    @property
    def _schema_out(self) -> Type[SpecializationOut]:
        return SpecializationOut

    @property
    def _schema_in(self) -> Type[SpecializationIn]:
        return SpecializationIn
