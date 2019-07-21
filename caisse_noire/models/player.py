import uuid
import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import (
    or_,
    Column,
    String,
    Boolean,
    DateTime
)
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
    def get_total_players_by_team(team_uuid: uuid) -> int:
        """
        """
        return db.session.query(Player).filter_by(
            team_uuid=team_uuid
        ).count()

    @staticmethod
    def get_all_players_by_team(team_uuid: uuid) -> list:
        """
        """
        return db.session.query(Player).filter(
            Player.team_uuid == team_uuid
        )

    @staticmethod
    def get_player_by_uuid(
        player_uuid,
    ):
        return db.session.query(Player).filter_by(
            uuid=player_uuid
        ).first()

    @staticmethod
    def get_player_by_name(
        players,
        filter,
    ):
        return players.filter(
            or_(
                Player.first_name.ilike(f'%%{filter}%%'),
                Player.last_name.ilike(f'%%{filter}%%'),
            )
        )

    @staticmethod
    def get_players_by_limit_per_page(
        players,
        limit
    ):
        return players.order_by(Player.created_date.asc()).limit(limit)

    @staticmethod
    def get_players_by_lastuuid(
        players,
        from_last_uuid,
        limit
    ):
        return players.filter(
            Player.created_date > from_last_uuid.created_date
        ).order_by(
            Player.first_name.asc()
        ).limit(
            limit
        )

    @staticmethod
    def get_player_fines_by_uuid(
        player_uuid: uuid
    ) -> PlayerFines:
        return db.session.query(
            PlayerFines
        ).filter(
            PlayerFines.player_uuid == player_uuid
        )

    @staticmethod
    def delete_player_fines(
        player_uuid: uuid,
    ):
        db.session.query(PlayerFines).filter_by(
            player_uuid=player_uuid
        ).delete()
        db.session.commit()

    @staticmethod
    def get_players_by_team(
        team_uuid,
    ):
        return db.session.query(Player).filter_by(team_uuid=team_uuid).all()

    @staticmethod
    def get_player_fine_cost(
        player_uuid,
    ):
        return db.session.query(
                func.sum(Fine.cost)
            ).join(
                PlayerFines, (Fine.uuid == PlayerFines.fine_uuid)
            ).join(
                Player, (Player.uuid == PlayerFines.player_uuid)
            ).filter(
                PlayerFines.player_uuid == player_uuid
            ).order_by(func.sum(Fine.cost)).limit(1).scalar()
