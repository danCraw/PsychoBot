from sqlalchemy import Column, String, Table, Integer, Boolean


from db.base import metadata

Psychologist = Table(
                'psychoapp_psychologist',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                Column("tg_link", String(65), nullable=False),
                Column("age", Integer, nullable=False),
                Column("description", String(1000), nullable=False),
                Column("photo", String(65), nullable=False),
                Column("meet_price", Integer, nullable=False),
                Column("average_score", Integer, nullable=False, default=0),
                Column("likes", Integer, nullable=False, default=0),
                Column("approved", Boolean, nullable=False)
                )
