from app import db
from sqlalchemy.dialects.postgresql import JSON, UUID

class Player(db.Model):
    __tablename__ = 'player'

    uuid = db.Column(UUID, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    banker = db.Column(db.Boolean(), unique=False, default=True)
    team_uuid = db.Column(db.String())
    password = db.Column(db.String())

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