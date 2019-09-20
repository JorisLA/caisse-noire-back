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

    @staticmethod
    def get_fines_other_page_from_list(
        fines: list,
        from_last_fine: object,
        page: int
    ) -> object:
        return fines.filter(
            Fine.created_date > from_last_fine.created_date
        ).order_by(
            Fine.label.asc()
        ).limit(
            page
        )

    @staticmethod
    def get_fines_limit_from_list(fines: list, page: int) -> object:
        return fines.order_by(
            Fine.created_date.asc()
        ).limit(
            page
        )

    @staticmethod
    def get_fine_by_label_from_list(fines: list, label: str) -> object:
        return fines.filter(
            Fine.label.like('%'+label+'%')
        )

    @staticmethod
    def get_fine_by_uuid(uuid: uuid) -> object:
        return db.session.query(Fine).filter_by(
            uuid=uuid
        ).first()

    @staticmethod
    def get_all_fines_by_team(team_uuid: uuid) -> object:
        return db.session.query(
            Fine
        ).filter(
            Fine.team_uuid == team_uuid
        )

    @staticmethod
    def get_total_fines_by_team(team_uuid: uuid) -> object:
        return db.session.query(Fine).filter_by(
            team_uuid=team_uuid
        ).count()

    @staticmethod
    def delete_fine(fine: object) -> None:
        db.session.delete(fine)
        db.session.commit()
