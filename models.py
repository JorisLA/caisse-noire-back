import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam

from app import db, text, func

Base = declarative_base()

""" PlayerFines = db.Table('PlayerFines', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('player_uuid', UUID, db.ForeignKey('player.uuid')),
    db.Column('fine_uuid', UUID, db.ForeignKey('fine.uuid'))
) """
class PlayerFines(db.Model):
    __tablename__ = 'PlayerFines'

    player_uuid = db.Column(UUID, db.ForeignKey('player.uuid'))
    fine_uuid = db.Column(UUID, db.ForeignKey('fine.uuid'))
    player_fines_id = db.Column(UUID, primary_key=True)

    fine = relationship("Fine", cascade="all,delete", backref="Fine")

TeamFines = db.Table('TeamFines',
    db.Column('team_uuid', UUID, db.ForeignKey('team.uuid')),
    db.Column('fine_uuid', UUID, db.ForeignKey('fine.uuid'))
)

class Team(db.Model):
    __tablename__ = 'team'

    uuid = db.Column(UUID, primary_key=True)
    label = db.Column(db.String())
    players = relationship("Player")
    fines = relationship("Fine", secondary=TeamFines,
        backref=db.backref('teams_fines', lazy=True))

    def __init__(
            self,
            uuid,
            label,
    ):
        self.uuid = uuid
        self.label = label

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)

    @staticmethod
    def get_team_by_uuid(
        team_uuid,
    ):
        return Team.query.filter_by(uuid=team_uuid).first()
    
    
class Player(db.Model):
    __tablename__ = 'player'

    uuid = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    banker = db.Column(db.Boolean(), unique=False, default=True)
    password = db.Column(db.String())
    team_uuid = db.Column(UUID, db.ForeignKey('team.uuid'))
    fines = relationship("PlayerFines", cascade="all,delete", backref="Fine")

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
        self.banker = banker
        self.team_uuid = team_uuid
        self.password = password

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)

    @staticmethod
    def get_player_by_uuid(
        player_uuid,
    ):
        return Player.query.filter_by(uuid=player_uuid).first()

    @staticmethod
    def get_player_by_email(
        player_email,
    ):
        return Player.query.filter_by(email=player_email).first()

    @staticmethod
    def delete_player(
        player,
    ):
        db.session.delete(player)
        db.session.commit()

    @staticmethod
    def get_players(
        team_uuid,
        _sort,
        _order,
        _filter,
        _currentPage,
        _perPage,
        _offset,
    ):
        PLAYERS = []
        _query = """
            SELECT sum(fine.cost) AS total,
                player.uuid,
                player.first_name,
                player.last_name,
                count(*) OVER() AS full_count
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
            for player in db.engine.execute(
                query,
                team_uuid=team_uuid,
                _filter='%' + _filter + '%',
            ).fetchall():
                PLAYERS.append({
                    'uuid': player.uuid,
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'total': player.total,
                    'full_count': player.full_count
                })
            return PLAYERS

        if int(_currentPage) == 1:
            if _sort and _order:
                _query = _query + """
                        GROUP BY player.uuid
                        ORDER BY {0} {1}
                        LIMIT :_perPage
                    """.format(_sort, _order)
                query = text(_query)
                for player in db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _perPage=_perPage,
                ).fetchall():
                    PLAYERS.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                        'full_count': player.full_count
                    })
                return PLAYERS
            else:
                _query = _query + """
                        GROUP BY player.uuid
                        LIMIT :_perPage
                    """
                query = text(_query)
                for player in db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _perPage=_perPage,
                ).fetchall():
                    PLAYERS.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                        'full_count': player.full_count
                    })
                return PLAYERS
        else:
            if _sort and _order:
                _query = _query + """
                        GROUP BY player.uuid
                        ORDER BY {0} {1}
                        OFFSET :_offset
                    """.format(_sort, _order)
                query = text(_query)
                for player in db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _offset=_offset,
                ).fetchall():
                    PLAYERS.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                        'full_count': player.full_count
                    })
                return PLAYERS
            else:
                _query = _query + """
                        GROUP BY player.uuid
                        OFFSET :_offset
                    """
                query = text(_query)
                for player in db.engine.execute(
                    query,
                    team_uuid=team_uuid,
                    _offset=_offset,
                ).fetchall():
                    PLAYERS.append({
                        'uuid': player.uuid,
                        'first_name': player.first_name,
                        'last_name': player.last_name,
                        'total': player.total,
                        'full_count': player.full_count
                    })
                return PLAYERS

class Fine(db.Model):
    __tablename__ = 'fine'

    uuid = db.Column(UUID, primary_key=True)
    label = db.Column(db.String())
    cost = db.Column(db.Integer())

    def __init__(
            self,
            uuid,
            label,
            cost,
    ):
        self.uuid = uuid
        self.label = label
        self.cost = cost

    @staticmethod
    def get_fine_by_uuid(
        fine_uuid,
    ):
        return Fine.query.filter_by(uuid=fine_uuid).first()

    @classmethod
    def get_fines(
        cls,
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
                cls.uuid,
                cls.label,
                cls.cost,
                TeamFines.c.team_uuid
                ).join(
                    TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                ).filter(
                    TeamFines.c.team_uuid == user_team_uuid
                ).group_by(
                    TeamFines.c.team_uuid,
                    cls.uuid
                ):
                FINES.append({
                    'value': fine.uuid,
                    'text': fine.label
                })
        else:
            if _filter:
                fines = db.session.query(
                    cls.uuid,
                    cls.label,
                    cls.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid,
                        cls.label.like('%'+_filter+'%')
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
                    cls.uuid,
                    cls.label,
                    cls.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid
                    ).group_by(
                        TeamFines.c.team_uuid,
                        cls.uuid
                    ).order_by(
                        cls.getOrder(cls,ordering)
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
                    cls.uuid,
                    cls.label,
                    cls.cost,
                    TeamFines.c.team_uuid
                    ).join(
                        TeamFines, (Fine.uuid==TeamFines.c.fine_uuid)
                    ).filter(
                        TeamFines.c.team_uuid == user_team_uuid
                    ).group_by(
                        TeamFines.c.team_uuid,
                        cls.uuid
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
                FINES[0]['full_count'] = cls.get_count(
                    db.session.query(TeamFines).filter_by(team_uuid=user_team_uuid)
                )
        return FINES

    def getOrder(
        self,
        order
    ):
        return {
            'labelasc':self.label.asc(),
            'labeldesc':self.label.desc(),
            'costasc':self.cost.asc(),
            'costdesc':self.cost.desc(),
        }.get(order)

    def get_count(q):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    @staticmethod
    def create_fine(
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

    @staticmethod
    def update_fine(
        post_data,
        fine,
    ):
        fine.label = post_data['label']
        fine.cost = post_data['cost']
        db.session.commit()

    @staticmethod
    def delete_fine(
        fine,
    ):
        db.session.delete(fine)
        db.session.commit()