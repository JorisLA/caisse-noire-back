import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy import Column
from sqlalchemy import String

from caisse_noire.models.db_base import DBBase

class Team(DBBase):
    __tablename__ = 'team'

    uuid = Column(UUID, primary_key=True)
    label = Column(String)
    players = relationship("Player")

    def __init__(
            self,
            uuid,
            label,
    ):
        self.uuid = uuid
        self.label = label

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
