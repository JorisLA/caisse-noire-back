from app import db
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

PlayerFines = db.Table('PlayerFines',
    db.Column('player_uuid', UUID, db.ForeignKey('player.uuid')),
    db.Column('fine_uuid', UUID, db.ForeignKey('fine.uuid'))
)

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
    
    
class Player(db.Model):
    __tablename__ = 'player'

    uuid = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    banker = db.Column(db.Boolean(), unique=False, default=True)
    password = db.Column(db.String())
    team_uuid = db.Column(UUID, db.ForeignKey('team.uuid'))
    fines = relationship("Fine", secondary=PlayerFines,
        backref=db.backref('players_fines', lazy=True))

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

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)