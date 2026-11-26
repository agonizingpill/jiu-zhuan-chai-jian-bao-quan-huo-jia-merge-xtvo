from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


rack_merges = Table('rack_merges', metadata,
    Column('code', String(64), primary_key=True),
    Column('candidate', String(160), ForeignKey('rack_candidates.code'), nullable=False, unique=True),
    Column('rack', String(160), nullable=False, unique=True),
    Column('pieces', Integer, nullable=False),
    Column('operator_note', String(160), nullable=False),
)
