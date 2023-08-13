from sqlalchemy import Column, String, Table, ForeignKey, Integer

from db.base import metadata

Schedule = Table(
    'psychoapp_schedule',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("day_of_the_week", String(65), nullable=False),
    Column("psychologist_id", Integer, ForeignKey("psychoapp_psychologist.id", ondelete="CASCADE"), nullable=True)
    )
