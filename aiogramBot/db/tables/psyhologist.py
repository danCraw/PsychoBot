from sqlalchemy import Column, String, Table, Integer

from aiogramBot.db.base import metadata

Psychologist = Table(
    'psychoapp_psychologist',
    metadata,
    Column('id', Integer, primary_key=True),
    Column("name", String(65), nullable=False),
    Column('tg_link', String(65), nullable=False),
    Column('age', Integer, nullable=False),
    Column('description', String(1000), nullable=False),
    Column('photo', String(100), nullable=False),
    Column('meet_price', Integer, nullable=False),
    Column('likes', Integer, nullable=False),
)
