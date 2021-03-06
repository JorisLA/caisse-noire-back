import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy import Column
from sqlalchemy import String

from caisse_noire.models.db_base import DBBase
from database import db


class Team(db.Model):
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

    @staticmethod
    def get_team_by_uuid(
        self,
        team_uuid,
    ):
        return db.session.query(Team).filter_by(uuid=team_uuid).first()
