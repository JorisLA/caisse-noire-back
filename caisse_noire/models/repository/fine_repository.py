import uuid

from flask import current_app

from caisse_noire.models.fine import Fine
from caisse_noire.models.team import Team
from caisse_noire.models.player import Player, PlayerFines
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

    def get_all_fines_by_team(
        self,
        team_uuid,
        filters,
    ):
        fines = Fine.get_all_fines_by_team(team_uuid)

        total_rows = Fine.get_all_fines_by_team(team_uuid)

        # FILTER BY LABEL
        if filters.get('filter'):
            return {
                'fines': Fine.get_fine_by_label_from_list(
                    fines,
                    filters.get('filter'),
                ),
                'total_rows': total_rows,
            }

        if int(filters.get('currentPage')) == 1:
            fines = Fine.get_fines_limit_from_list(
                fines,
                int(filters.get('perPage')),
            )
        else:
            from_last_fine = Fine.get_fine_by_uuid(
                uuid=filters.get('lastUuid'),
            )
            if not from_last_fine:
                raise EntityNotFound(error_code='last_fine_not_found')
            fines = Fine.get_fines_other_page_from_list(
                fines,
                from_last_fine,
                int(filters.get('perPage')),
            )
        return {
            'fines': fines,
            'total_rows': total_rows,
        }

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
            self,
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
        payload: dict,
    ) -> None:
        if not payload['banker']:
            raise AuthorizationError(error_code='player_unauthorized')

        fine = Fine.get_fine_by_uuid(uuid=payload['fine_uuid'])

        if not fine:
            raise EntityNotFound(error_code='fine_not_found')

        if not payload['cost'] or not payload['label']:
            raise ModelCreationError(error_code='missing_parameter')

        fine.label = payload['label']
        fine.cost = payload['cost']
        db.session.commit()

    def delete_fine(
        self,
        payload: dict,
    ) -> None:
        if not payload['banker']:
            raise AuthorizationError(error_code='player_unauthorized')

        fine = Fine.get_fine_by_uuid(uuid=payload['fine_uuid'])

        if not fine:
            raise EntityNotFound(error_code='fine_not_found')

        Player.delete_player_fines_by_uuid(fine_uuid=fine.uuid)
        Fine.delete_fine(fine=fine)
