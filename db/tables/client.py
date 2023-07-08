from sqlalchemy import Column, String, Table, Integer, ForeignKey

from db.base import metadata

Client = Table(
    'psychoapp_client',
    metadata,
    Column("tg_id", Integer, primary_key=True),
    Column("name", String(65), nullable=False),
    Column("tariff_id", String(65), ForeignKey("psychoapp_tariff.name"), nullable=True),
    Column("remaining_meets", Integer, nullable=False)
)
