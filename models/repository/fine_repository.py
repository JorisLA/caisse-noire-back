import uuid

from flask_sqlalchemy import SQLAlchemy

from models.fine import Fine
from models.team import Team
from models.player import PlayerFines
from __main__ import app
db = SQLAlchemy(app)

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
        fines = db.session.query(Fine
            ).filter(
                Fine.team_uuid==team_uuid
            )
        if for_player_view:
            return {
                'fines' : fines,
            }
        else:
            total_rows = db.session.query(Fine).filter_by(team_uuid=team_uuid).count()
            fines = db.session.query(Fine
                ).filter(
                    Fine.team_uuid==team_uuid
                )
            if additional_filters.get('lastUuid') != '':
                from_object = db.session.query(Fine).filter_by(uuid=additional_filters.get('lastUuid')).first()
            # FILTER BY LABEL
            if additional_filters.get('filter'):
                fines = fines.filter(
                    Fine.label.like('%'+additional_filters.get('filter')+'%')
                )
                return {
                    'fines' : fines,
                    'total_rows' : total_rows,
                }

            if int(additional_filters.get('currentPage')) == 1:
                fines = fines.order_by(Fine.created_date.asc()).limit(int(additional_filters.get('perPage')))
            else:
                fines = fines.filter(
                    Fine.created_date > from_object.created_date
                ).order_by(
                    Fine.label.asc()
                ).limit(
                    int(additional_filters.get('perPage'))
                )
            return {
                'fines' : fines,
                'total_rows' : total_rows,
            }

    def getOrder(
        self,
        order,
    ):
        return {
            'labelasc':Fine.label.asc(),
            'labeldesc':Fine.label.desc(),
            'costasc':Fine.cost.asc(),
            'costdesc':Fine.cost.desc(),
        }.get(order)

    def create_fine(
        self,
        post_data,
        team,
    ):
        response_object = {}
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
        db.session.query(PlayerFines).filter(PlayerFines.fine_uuid==fine.uuid).delete()
        db.session.commit()
        db.session.delete(fine)
        db.session.commit()
