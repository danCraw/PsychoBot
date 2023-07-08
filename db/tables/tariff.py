from sqlalchemy import Column, String, Table, Integer

from db.base import metadata

Tariff = Table(
    'psychoapp_tariff',
    metadata,
    Column("name", String(65), nullable=False, primary_key=True),
    Column("meets", Integer, nullable=False),
)
