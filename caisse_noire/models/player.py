import uuid
import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from caisse_noire.models.db_base import DBBase
from database import db


class PlayerFines(db.Model):
    __tablename__ = 'PlayerFines'

    player_uuid = Column(UUID, ForeignKey('player.uuid'))
    fine_uuid = Column(UUID, ForeignKey('fine.uuid'))
    player_fines_id = Column(UUID, primary_key=True)

    fine = relationship("Fine", cascade="all,delete", backref="Fine")


class Player(db.Model):
    __tablename__ = 'player'

    uuid = Column(UUID, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    banker = Column(Boolean, unique=False, default=True)
    password = Column(String)
    team_uuid = Column(UUID, ForeignKey('team.uuid'))
    fines = relationship("PlayerFines", cascade="all,delete", backref="Fine")
    created_date = Column(
        DateTime, default=datetime.datetime.utcnow, index=True)

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

    # def __repr__(self):
    #    return '<uuid {}>'.format(self.uuid)

    def to_dict(self):
        """
        """
        info = {
            'date': self.created_date,
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

    @staticmethod
    def get_total_players_by_team(self):
        """
        """
        total_rows = db.session.query(Player).filter_by(
            team_uuid=team_uuid
        ).count()
