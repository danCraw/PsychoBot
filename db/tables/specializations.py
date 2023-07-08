from sqlalchemy import Column, String, Table, Integer, Boolean


from db.base import metadata

Specialization = Table(
                'psychoapp_specialization',
                metadata,
                Column("id", Integer, primary_key=True),
                Column("name", String(65), nullable=False),
                )
