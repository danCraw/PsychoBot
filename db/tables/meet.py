from sqlalchemy import Column, Table, Integer, ForeignKey, DateTime

from db.base import metadata

Meet = Table(
    'psychoapp_meet',
    metadata,
    Column("id", Integer,  primary_key=False),
    Column("time_start", DateTime),
    Column("time_end", DateTime),
    Column("day_of_the_week_id", Integer, ForeignKey("psychoapp_schedule.id"), nullable=True),
    Column("client_id", Integer, ForeignKey("psychoapp_client.id"), nullable=True)
)
