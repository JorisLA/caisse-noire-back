import uuid
import collections

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.sql import select, text

from caisse_noire.models.player import Player, PlayerFines
from caisse_noire.models.fine import Fine
from caisse_noire.models.team import Team
from caisse_noire.models.repository.team_repository import TeamModelRepository
from app import db
from caisse_noire.common.password import Passwords
from caisse_noire.common.exceptions.database_exceptions import (
    DatabaseError,
    ModelCreationError,
    ModelUpdateError,
    EntityNotFound,
)
from caisse_noire.common.exceptions.authorization_exceptions import (
    AuthorizationError,
)
from caisse_noire.common.uuid_checker import is_uuid


class PlayerModelRepository(object):
    """
    """

    def update_player_fine(
        self,
        payload: dict,
    ) -> dict:
        if not payload['banker']:
            raise AuthorizationError(error_code='player_unauthorized')

        player = Player.get_player_by_uuid(player_uuid=payload['player_uuid'])

        if not player:
            raise EntityNotFound(error_code='player_not_found')

        if not payload['fine_uuid']:
            raise ModelCreationError(error_code='missing_parameter')

        fine = Fine.get_fine_by_uuid(uuid=payload['fine_uuid'])

        if not fine:
            raise EntityNotFound(error_code='fine_not_found')

        player_fine = PlayerFines(player_fines_id=str(uuid.uuid4()))
        player_fine.fine = fine
        player.fines.append(player_fine)
        db.session.commit()

        return player.to_dict()

    def signup_player(
        self,
        player_info,
    ):
        player_uuid = str(uuid.uuid4())

        password = player_info.get('password', None)
        first_name = player_info.get('first_name', None)
        last_name = player_info.get('last_name', None)
        email = player_info.get('email', None)
        add_team = player_info.get('add_team', None)
        team_uuid = player_info.get('get_team', None)

        if (
            (password is None or not password) or
            (first_name is None or not first_name) or
            (last_name is None or not last_name) or
            (email is None or not email) or
            (
                (add_team is None) and (team_uuid is None)
            )
        ):
            raise ModelCreationError(error_code='missing_parameter')

        if (
            (add_team is not None and not add_team) or
            (team_uuid is not None and not is_uuid(team_uuid))
        ):
            raise ModelCreationError(error_code='invalid_parameter')

        if not Passwords.is_password_valid(password):
            raise ModelCreationError(error_code='invalid_password')

        if 'add_team' in player_info:
            banker = True
            team_uuid = TeamModelRepository.create_team(
                self,
                team_name=add_team,
            )
        else:
            team = Team.get_team_by_uuid(
                self,
                team_uuid=team_uuid,
            )
            if not team:
                raise EntityNotFound(error_code='team_not_found')
            banker = False

        player = Player(
            uuid=player_uuid,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Passwords.hash_password(password),
            banker=banker,
            team_uuid=team_uuid,
        )

        db.session.add(player)
        db.session.commit()

        return {
            "player_uuid": player_uuid,
            "team_uuid": team_uuid
        }

    def signin_player(
        self,
        player_info,
    ):
        password = player_info.get('password', None)
        email = player_info.get('email', None)

        if (
            (password is None or not password) or
            (email is None or not email)
        ):
            raise ModelCreationError(error_code='missing_parameter')

        player = Player.get_player_by_email(player_email=email)

        if not player:
            raise EntityNotFound(error_code='player_not_found')

        token = Passwords.generate_token(player, password)

        return jsonify(
            {
                'token': token.decode('UTF-8'),
                'banker': player.banker,
            }
        )

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
        total_players = Player.get_total_players_by_team(team_uuid)
        if not total_players:
            raise EntityNotFound(error_code='team_not_found')
        players = Player.get_all_players_by_team(team_uuid)

        if (
            additional_filters.get('lastUuid') and
            additional_filters.get('lastUuid') != ''
        ):
            from_last_uuid = Player.get_player_by_uuid(
                player_uuid=additional_filters.get('lastUuid')
            )
            if not from_last_uuid:
                raise EntityNotFound(error_code='player_not_found')

        # FILTER BY FIRST NAME OR LAST NAME
        if (
            additional_filters.get('filter') and
            additional_filters.get('filter') != ''
        ):
            players = Player.get_player_by_name(
                players=players,
                filter=additional_filters.get('filter')
            )
            return {
                'players': players,
                'total_rows': total_players,
            }

        # FIRST PAGE
        if int(additional_filters.get('currentPage')) == 1:
            players = Player.get_players_by_limit_per_page(
                players=players,
                limit=int(additional_filters.get('perPage'))
            )
        else:
            players = Player.get_players_by_lastuuid(
                players=players,
                from_last_uuid=from_last_uuid,
                limit=int(additional_filters.get('perPage'))
            )
        return {
            'players': players,
            'total_rows': total_players,
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
                    LEFT OUTER JOIN "PlayerFines" ON
                        player.uuid = "PlayerFines".player_uuid
                    LEFT OUTER JOIN fine ON
                        "PlayerFines".fine_uuid = fine.uuid
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
        player_uuid: uuid,
    ) -> collections:
        result = []

        player = Player.get_player_by_uuid(player_uuid=player_uuid)

        if not player:
            raise EntityNotFound(error_code='player_not_found')

        player_fines = Player.get_player_fines_by_uuid(
            player_uuid=player_uuid
        )

        for player_fine in player_fines:
            result.append(
                player_fine.fine.label,
            )
        # return the count of each fines a player has
        # ex: {'toto':2, 'titi':1}
        final_result = collections.Counter(result)
        return final_result

    def delete_player_fines(
        self,
        banker: bool,
        player_uuid: uuid,
    ) -> bool:
        if not banker:
            raise AuthorizationError(error_code='player_unauthorized')

        player = Player.get_player_by_uuid(player_uuid=player_uuid)

        if not player:
            raise EntityNotFound(error_code='player_not_found')

        Player.delete_player_fines(player_uuid)

        return True

    def send_fines_to_players_email(
        self,
        banker: bool,
        team_uuid: uuid,
    ) -> None:
        if not banker:
            raise AuthorizationError(error_code='player_unauthorized')

        team = Team.get_team_by_uuid(team_uuid=team_uuid)

        if not team:
            raise EntityNotFound(error_code='team_not_found')

        players = Player.get_players_by_team(
            team_uuid=team_uuid
        )

        for player in players:
            fine_cost = Player.get_player_fine_cost(player_uuid=player.uuid)
            mail.send_email(
                from_email='admin@caissenoire.com',
                to_email=player.email,
                subject='Caisse noire payment',
                text='You have to pay {} € this month'.format(fine_cost),
            )
