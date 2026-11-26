from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON, String, Table

from core.db import metadata


yard_scores = Table('yard_scores', metadata,
    Column('stack', String(64), ForeignKey('brick_stacks.code'), primary_key=True),
    Column('score', Float, nullable=True),
    Column('basis', JSON, nullable=False),
    Column('token', String(32), nullable=False),
    Column('updated', DateTime(timezone=True), nullable=False),
)
