import uuid

from app import db, text, func
from models.fine import Fine
from models.team import TeamFines, Team

class FineModelRepository(object):
    """
    """

    def get_fine_by_uuid(
        self,
        fine_uuid,
    ):
        return Fine.query.filter_by(uuid=fine_uuid).first()

    def get_all_fines_by_team(
        self,
        team_uuid,
        additional_filters,
        for_player_view=False,
    ):
        FINES = []
        if for_player_view:
            for fine in db.session.query(
                Fine.uuid,
                Fine.label,
                Fine.cost,
                TeamFines.c.team_uuid
                ).join(
                    TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                ).filter(
                    TeamFines.c.team_uuid == team_uuid
                ).group_by(
                    TeamFines.c.team_uuid,
                    Fine.uuid
                ):
                FINES.append({
                    'value': fine.uuid,
                    'text': fine.label
                })
        else:
            total_rows = self.get_count(
                db.session.query(TeamFines).filter_by(team_uuid=team_uuid)
            )
            fines = db.session.query(
                Fine,
                TeamFines.c.team_uuid
                ).join(
                    TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                ).filter(
                    TeamFines.c.team_uuid == team_uuid
                )
            if additional_filters.get('lastUuid') != '':
                from_object = Fine.query.filter_by(uuid=additional_filters.get('lastUuid')).first()
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

    def get_count(
        self,
        q,
    ):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def create_fine(
        self,
        post_data,
        team,
    ):
        response_object = {}
        fine = Fine(
            uuid=str(uuid.uuid4()),
            label=post_data['label'],
            cost=post_data['cost']
        )
        db.session.add(fine)
        fine.teams_fines.append(team)
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
        db.session.delete(fine)
        db.session.commit()