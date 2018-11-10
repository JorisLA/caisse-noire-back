import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import bindparam

from app import db

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

    fine = relationship("Fine")

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
    fines = relationship("PlayerFines")

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
    ):
        FINES = []
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
                'uuid': fine.uuid,
                'label': fine.label,
                'cost': fine.cost
            })
        return FINES

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