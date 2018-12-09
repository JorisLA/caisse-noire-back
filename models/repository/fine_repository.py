import uuid

from app import db, text, func
from models.fine import Fine
from models.team import TeamFines

class FineModelRepository(object):
    """
    """

    def get_fine_by_uuid(
        self,
        fine_uuid,
    ):
        return Fine.query.filter_by(uuid=fine_uuid).first()

    def get_fines(
        self,
        user_team_uuid,
        _sort,
        _order,
        _filter,
        _currentPage,
        _perPage,
        _offset,
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
                    TeamFines.c.team_uuid == user_team_uuid
                ).group_by(
                    TeamFines.c.team_uuid,
                    Fine.uuid
                ):
                FINES.append({
                    'value': fine.uuid,
                    'text': fine.label
                })
        else:
            if _filter:
                fines = db.session.query(
                    Fine.uuid,
                    Fine.label,
                    Fine.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid,
                        Fine.label.like('%'+_filter+'%')
                    )
                for fine in fines:
                    FINES.append({
                        'uuid': fine.uuid,
                        'label': fine.label,
                        'cost': fine.cost,
                    })
            elif _sort and _order:
                ordering = '{}{}'.format(_sort,_order)
                fines = db.session.query(
                    Fine.uuid,
                    Fine.label,
                    Fine.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid
                    ).group_by(
                        TeamFines.c.team_uuid,
                        Fine.uuid
                    ).order_by(
                        self.getOrder(ordering)
                    ).paginate(
                        int(_currentPage),
                        int(_perPage),
                        False
                    )
                for fine in fines.items:
                    FINES.append({
                        'uuid': fine.uuid,
                        'label': fine.label,
                        'cost': fine.cost,
                    })
            else:
                fines = db.session.query(
                    Fine.uuid,
                    Fine.label,
                    Fine.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid
                    ).group_by(
                        TeamFines.c.team_uuid,
                        Fine.uuid
                    ).paginate(
                        int(_currentPage),
                        int(_perPage),
                        False
                    )
                for fine in fines.items:
                    FINES.append({
                        'uuid': fine.uuid,
                        'label': fine.label,
                        'cost': fine.cost,
                    })
            if FINES:
                FINES[0]['full_count'] = self.get_count(
                    db.session.query(TeamFines).filter_by(team_uuid=user_team_uuid)
                )
        return FINES

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