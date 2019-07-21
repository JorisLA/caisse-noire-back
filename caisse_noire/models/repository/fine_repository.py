import uuid

from flask import current_app

from caisse_noire.models.fine import Fine
from caisse_noire.models.team import Team
from caisse_noire.models.player import PlayerFines
from caisse_noire.common.exceptions.database_exceptions import (
    DatabaseError,
    ModelCreationError,
    ModelUpdateError,
    EntityNotFound,
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)
from app import db


class FineModelRepository(object):
    """
    """

    def get_fine_by_uuid(
        self,
        fine_uuid,
    ):
        return db.session.query(Fine).filter_by(uuid=fine_uuid).first()

    def get_all_fines_by_team(
        self,
        team_uuid,
        additional_filters,
        for_player_view=False,
    ):
        fines = db.session.query(
            Fine
        ).filter(
            Fine.team_uuid == team_uuid
        )
        if for_player_view:
            return {
                'fines': fines,
            }
        else:
            total_rows = db.session.query(Fine).filter_by(
                team_uuid=team_uuid).count()
            fines = db.session.query(Fine
                                     ).filter(
                Fine.team_uuid == team_uuid
            )
            if additional_filters.get('lastUuid') != '':
                from_object = db.session.query(Fine).filter_by(
                    uuid=additional_filters.get('lastUuid')).first()
            # FILTER BY LABEL
            if additional_filters.get('filter'):
                fines = fines.filter(
                    Fine.label.like('%'+additional_filters.get('filter')+'%')
                )
                return {
                    'fines': fines,
                    'total_rows': total_rows,
                }

            if int(additional_filters.get('currentPage')) == 1:
                fines = fines.order_by(Fine.created_date.asc()).limit(
                    int(additional_filters.get('perPage')))
            else:
                fines = fines.filter(
                    Fine.created_date > from_object.created_date
                ).order_by(
                    Fine.label.asc()
                ).limit(
                    int(additional_filters.get('perPage'))
                )
            return {
                'fines': fines,
                'total_rows': total_rows,
            }

    def getOrder(
        self,
        order,
    ):
        return {
            'labelasc': Fine.label.asc(),
            'labeldesc': Fine.label.desc(),
            'costasc': Fine.cost.asc(),
            'costdesc': Fine.cost.desc(),
        }.get(order)

    def create_fine(
        self,
        banker: bool,
        post_data: dict,
        team_uuid: uuid,
    ) -> None:
        if not banker:
            raise AuthorizationError(error_code='player_unauthorized')

        cost = post_data.get('cost', None)
        label = post_data.get('label', None)

        if (
            (cost is None or not cost) or
            (label is None or not label)
        ):
            raise ModelCreationError(error_code='missing_parameter')

        team = Team.get_team_by_uuid(
            team_uuid=team_uuid
        )

        if not team:
            raise EntityNotFound(error_code='team_not_found')

        fine = Fine(
            uuid=str(uuid.uuid4()),
            label=post_data['label'],
            cost=post_data['cost'],
            team_uuid=team.uuid
        )
        db.session.add(fine)
        db.session.commit()

    def update_fine(
        self,
        post_data,
        fine,
    ):
        fine.label = post_data['label']
        fine.cost = post_data['cost']
        db.session.commit()

    def delete_fine(
        self,
        fine,
    ):
        db.session.query(PlayerFines).filter(
            PlayerFines.fine_uuid == fine.uuid
        ).delete()
        db.session.commit()
        db.session.delete(fine)
        db.session.commit()
