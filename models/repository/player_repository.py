import uuid
import collections

from sqlalchemy import or_
from sqlalchemy.sql import select

from app import db, text, func
from models.player import Player, PlayerFines
from models.fine import Fine

class PlayerModelRepository(object):
    """
    """

    def update_player_fine(
        self,
        player,
        fine,
    ):
        association = PlayerFines(player_fines_id=str(uuid.uuid4()))
        association.fine = fine
        player.fines.append(association)
        db.session.commit()
        return player.to_dict()

    def get_players_by_team(
        self,
        team_uuid,
    ):
        return Player.query.filter_by(team_uuid=team_uuid).all()

    def get_player_by_uuid(
        self,       
        player_uuid,
    ):
        return Player.query.filter_by(uuid=player_uuid).first()

    def get_player_by_email(
        self,
        player_email,
    ):
        return Player.query.filter_by(email=player_email).first()

    def create_player(
        self,
        player_info,
    ):
        player_uuid = str(uuid.uuid4())
        player = Player(
            uuid=player_uuid,
            first_name=player_info['first_name'],
            last_name=player_info['last_name'],
            email=player_info['email'],
            password=player_info['pw_hash'],
            banker=player_info['banker'],
            team_uuid=player_info['team_uuid'],
        )
        db.session.add(player)
        db.session.commit()
        return player_uuid

    def delete_player(
        self,
        player,
    ):
        db.session.delete(player)
        db.session.commit()

    def get_all_players_from_team(
        self,
        team_uuid,
        additional_filters,
    ):
        total_rows = Player.query.filter_by(team_uuid=team_uuid).count()
        players = db.session.query(Player).filter(
            Player.team_uuid==team_uuid
        )
        if additional_filters.get('lastUuid') != '':
            from_object = Player.query.filter_by(uuid=additional_filters.get('lastUuid')).first()
        # FILTER BY FIRST NAME OR LAST NAME
        if additional_filters.get('filter') is not None:
            players = players.filter(
                or_(
                    Player.first_name.ilike('%%%s%%' % additional_filters.get('filter')),
                    Player.last_name.ilike('%%%s%%' % additional_filters.get('filter')),
                )
            )
            return {
                'players' : players,
                'total_rows' : total_rows,
            }


        # FIRST PAGE
        if int(additional_filters.get('currentPage')) == 1:
            players = players.order_by(Player.created_date.asc()).limit(int(additional_filters.get('perPage')))
        else:
            players = players.filter(
                Player.created_date > from_object.created_date
            ).order_by(
                Player.first_name.asc()
            ).limit(
                int(additional_filters.get('perPage'))
            )
        return {
            'players' : players,
            'total_rows' : total_rows,
        }

    def get_players(
        self,
        team_uuid,
        _sort,
        _order,
        _filter,
        _currentPage,
        _perPage,
        _offset,
    ):
        final_result = []
        _query = """
            SELECT sum(fine.cost) AS total,
                player.uuid,
                player.first_name,
                player.last_name
                    FROM player
                    LEFT OUTER JOIN "PlayerFines" ON player.uuid = "PlayerFines".player_uuid
                    LEFT OUTER JOIN fine ON "PlayerFines".fine_uuid = fine.uuid
                    JOIN team ON player.team_uuid = team.uuid
                    WHERE team.uuid = :team_uuid
        """
        if _filter:
            _query = _query + """
                    AND (
                        player.first_name LIKE :_filter
                        OR player.last_name LIKE :_filter
                    )
                    GROUP BY player.uuid
                """
            query = text(_query)
            results = db.engine.execute(
                query,
                team_uuid=team_uuid,
                _filter='%' + _filter + '%',
            ).fetchall()
            for player in results:
                final_result.append({
                    'uuid': player.uuid,
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'total': player.total,
                })
            return final_result

        if int(_currentPage) == 1:
            if _sort and _order:
                _query = _query + """
                        GROUP BY player.uuid
                        ORDER BY {0} {1}
                        LIMIT :_perPage
                    """.format(_sort, _order)
                query = text(_query)
                results = db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _perPage=_perPage,
                ).fetchall()
                for player in results:
                    final_result.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                    })
                return final_result
            else:
                _query = _query + """
                        GROUP BY player.uuid
                        LIMIT :_perPage
                    """
                query = text(_query)
                results = db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _perPage=_perPage,
                ).fetchall()
                for player in results:
                    final_result.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                    })
                return final_result
        else:
            if _sort and _order:
                _query = _query + """
                        GROUP BY player.uuid
                        ORDER BY {0} {1}
                        OFFSET :_offset
                    """.format(_sort, _order)
                query = text(_query)            
                results = db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _offset=_offset,
                ).fetchall()
                for player in results:
                    final_result.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                    })
                return final_result
            else:
                _query = _query + """
                        GROUP BY player.uuid
                        OFFSET :_offset
                    """
                query = text(_query)
                results = db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _offset=_offset,
                ).fetchall()
                for player in results:
                    final_result.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total
                    })
                return final_result

    def get_player_fines(
        self,
        player_uuid,
    ):     
        result = []
        fines = db.session.query(
                PlayerFines
            ).filter(PlayerFines.player_uuid==player_uuid)
        for fine in fines:    
            result.append(
                fine.fine.label,
            )
        final_result = collections.Counter(result)
        return final_result

    def get_player_fine_cost(
        self,
        player_uuid,
    ):
        return db.session.query(
            func.sum(Fine.cost)
        ).join(
            PlayerFines, (Fine.uuid==PlayerFines.fine_uuid)
        ).join(
            Player, (Player.uuid==PlayerFines.player_uuid)
        ).filter(PlayerFines.player_uuid==player_uuid).order_by(func.sum(Fine.cost)).limit(1).scalar()

    def delete_players_fines(
        self,
        players,
    ):
        for player in players:
            player.fines = []
        db.session.commit()

    def delete_player_fines(
        self,
        player,
    ):
        PlayerFines.query.filter_by(player_uuid=player.uuid).delete()
        db.session.commit()
