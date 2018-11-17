"""empty message

Revision ID: bb0d15c584d7
Revises: 
Create Date: 2018-10-28 19:53:06.109240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bb0d15c584d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fine',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('team',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('TeamFines',
    sa.Column('team_uuid', postgresql.UUID(), nullable=True),
    sa.Column('fine_uuid', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['fine_uuid'], ['fine.uuid'], ),
    sa.ForeignKeyConstraint(['team_uuid'], ['team.uuid'], )
    )
    op.create_table('player',
    sa.Column('uuid', postgresql.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('banker', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('team_uuid', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['team_uuid'], ['team.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('PlayerFines',
    sa.Column('player_uuid', postgresql.UUID(), nullable=True),
    sa.Column('fine_uuid', postgresql.UUID(), nullable=True),
    sa.Column('player_fines_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['fine_uuid'], ['fine.uuid'], ),
    sa.ForeignKeyConstraint(['player_uuid'], ['player.uuid'], ),
    sa.PrimaryKeyConstraint('player_fines_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PlayerFines')
    op.drop_table('player')
    op.drop_table('TeamFines')
    op.drop_table('team')
    op.drop_table('fine')
    # ### end Alembic commands ###
