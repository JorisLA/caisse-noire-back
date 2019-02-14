import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam

from app import db, text, func
from models.db_base import Base

#PlayerFines = db.Table('TeamFines',
#    db.Column('player_uuid', UUID, db.ForeignKey('player.uuid')),
#    db.Column('fine_uuid', UUID, db.ForeignKey('fine.uuid'))
#)

class PlayerFines(db.Model):
    __tablename__ = 'PlayerFines'

    player_uuid = db.Column(UUID, db.ForeignKey('player.uuid'))
    fine_uuid = db.Column(UUID, db.ForeignKey('fine.uuid'))
    player_fines_id = db.Column(UUID, primary_key=True)

    fine = relationship("Fine", cascade="all,delete", backref="Fine")

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, autoincrement=True, index=True)
    uuid = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    banker = db.Column(db.Boolean(), unique=False, default=True)
    password = db.Column(db.String())
    team_uuid = db.Column(UUID, db.ForeignKey('team.uuid'))
    fines = relationship("PlayerFines", cascade="all,delete", backref="Fine")

    def __init__(
            self,
            uuid,
            first_name,
            last_name,
            email,
            banker,
            team_uuid,
            password,
    ):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.banker = banker
        self.team_uuid = team_uuid
        self.password = password

    #def __repr__(self):
    #    return '<uuid {}>'.format(self.uuid)

    def to_dict(self):
        """
        """
        info = {
            'uuid': self.uuid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'total': self._total_fines()
        }

        return info

    def _total_fines(self):
        """
        """
        return sum([fine.fine.cost for fine in self.fines])
