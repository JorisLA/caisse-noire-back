import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam

from app import db, text, func
from models.db_base import Base

TeamFines = db.Table('TeamFines',
    db.Column('team_uuid', UUID, db.ForeignKey('team.uuid')),
    db.Column('fine_uuid', UUID, db.ForeignKey('fine.uuid'))
)

class Team(db.Model):
    __tablename__ = 'team'

    uuid = db.Column(UUID, primary_key=True)
    label = db.Column(db.String())
    players = relationship("Player")
    fines = relationship("Fine", secondary=TeamFines,
        backref=db.backref('teams_fines', lazy=True))

    def __init__(
            self,
            uuid,
            label,
    ):
        self.uuid = uuid
        self.label = label

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
