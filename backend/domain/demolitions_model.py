from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


demolitions = Table('demolitions', metadata,
    Column('code', String(64), primary_key=True),
    Column('street', String(160), nullable=False),
    Column('survey', String(160), nullable=False),
    Column('load_grade', String(160), nullable=False),
    Column('allowed', Boolean, nullable=False),
)
