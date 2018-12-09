import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam

from app import db, text, func
from models.db_base import Base

class Fine(db.Model):
    __tablename__ = 'fine'

    uuid = db.Column(UUID, primary_key=True)
    label = db.Column(db.String())
    cost = db.Column(db.Integer())

    def __init__(
            self,
            uuid,
            label,
            cost,
    ):
        self.uuid = uuid
        self.label = label
        self.cost = cost

 