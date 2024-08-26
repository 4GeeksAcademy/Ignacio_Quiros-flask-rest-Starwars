"""empty message

Revision ID: b80a4e525a4f
Revises: 1227263db432
Create Date: 2024-08-23 09:56:08.142845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b80a4e525a4f'
down_revision = '1227263db432'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('planet', sa.String(length=30), nullable=True),
    sa.Column('birth_year', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('character_id')
    )
    op.create_table('planets',
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('duration_day', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('planet_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('spaceships',
    sa.Column('spaceship_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('lenght', sa.Integer(), nullable=True),
    sa.Column('cargo_capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('spaceship_id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('spaceship')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('character_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('planet', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('birth_year', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('character_id', name='character_pkey')
    )
    op.create_table('planet',
    sa.Column('planet_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('diameter', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('population', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('duration_day', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('planet_id', name='planet_pkey'),
    sa.UniqueConstraint('name', name='planet_name_key')
    )
    op.create_table('spaceship',
    sa.Column('spaceship_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('crew', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lenght', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cargo_capacity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('spaceship_id', name='spaceship_pkey'),
    sa.UniqueConstraint('name', name='spaceship_name_key')
    )
    op.drop_table('spaceships')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###