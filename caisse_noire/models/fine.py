import uuid
import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from caisse_noire.models.db_base import DBBase
from database import db


class Fine(db.Model):
    __tablename__ = 'fine'

    uuid = Column(UUID, primary_key=True)
    label = Column(String)
    cost = Column(Integer)
    created_date = Column(
        DateTime, default=datetime.datetime.utcnow, index=True)
    team_uuid = Column(UUID, ForeignKey('team.uuid'))

    def __init__(
            self,
            uuid,
            label,
            cost,
            team_uuid,
    ):
        self.uuid = uuid
        self.label = label
        self.cost = cost
        self.team_uuid = team_uuid

    def to_dict(self, for_player_view=False):
        """
        """
        if for_player_view:
            info = {
                'value': self.uuid,
                'text': self.label,
            }

            return info

        info = {
            'date': self.created_date,
            'uuid': self.uuid,
            'label': self.label,
            'cost': self.cost,
        }

        return info
