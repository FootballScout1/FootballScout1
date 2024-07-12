#!/usr/bin/python3
from models.base_model import Base
from sqlalchemy import Column, ForeignKey, Table

scout_club = Table('scout_club', Base.metadata,
    Column('scout_id', ForeignKey('scouts.id'), primary_key=True),
    Column('club_id', ForeignKey('clubs.id'), primary_key=True)
)

