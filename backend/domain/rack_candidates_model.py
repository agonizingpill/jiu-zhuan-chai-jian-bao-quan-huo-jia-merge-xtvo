from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


rack_candidates = Table('rack_candidates', metadata,
    Column('code', String(64), primary_key=True),
    Column('member', String(160), ForeignKey('brick_stacks.code'), nullable=False),
    Column('pair', String(160), ForeignKey('brick_stacks.code'), nullable=False),
    Column('cluster_size', Integer, nullable=False),
    Column('token', String(64), nullable=False, unique=True),
)
