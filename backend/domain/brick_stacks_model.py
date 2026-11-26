from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


brick_stacks = Table('brick_stacks', metadata,
    Column('code', String(64), primary_key=True),
    Column('origin', String(160), ForeignKey('demolitions.code'), nullable=False),
    Column('length', Float, nullable=False),
    Column('perforation', Float, nullable=False),
    Column('wet', Float, nullable=False),
    Column('weighed', Boolean, nullable=False),
    Column('pieces', Integer, nullable=False),
    Column('merged', Boolean, nullable=False),
    CheckConstraint('pieces > 0'),
    CheckConstraint('perforation between 0 and 1'),
)
