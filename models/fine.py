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

    def __init__(
            self,
            uuid,
            label,
            cost,
    ):
        self.uuid = uuid
        self.label = label
        self.cost = cost

    def to_dict(self):
        """
        """
        info = {
            'date': self.created_date,
            'uuid': self.uuid,
            'label': self.label,
            'cost': self.cost,
        }

        return info
