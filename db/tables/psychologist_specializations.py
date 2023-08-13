from sqlalchemy import Column, Table, Integer, ForeignKey


from db.base import metadata
from db.tables.psychologists import Psychologist
from db.tables.specializations import Specialization

Psychologist_specialization = Table(
                'psychoapp_specialization_psychologists_specializations',
                metadata,
                Column("psychologist_id", Integer, ForeignKey(Psychologist.columns.id), primary_key=True),
                Column("specialization_id", Integer, ForeignKey(Specialization.columns.id), nullable=False),
                )
