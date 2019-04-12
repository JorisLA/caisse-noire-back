import uuid
import datetime

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam, DateTime

from app import db, text, func
from models.db_base import Base

class Fine(db.Model):
    __tablename__ = 'fine'

    uuid = db.Column(UUID, primary_key=True)
    label = db.Column(db.String())
    cost = db.Column(db.Integer())
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow, index=True)
    team_uuid = db.Column(UUID, db.ForeignKey('team.uuid'))

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
