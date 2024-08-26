"""empty message

Revision ID: 6d5d1fdba230
Revises: 1da126de2f9a
Create Date: 2024-08-23 16:06:34.511165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d5d1fdba230'
down_revision = '1da126de2f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('spaceships', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model', sa.String(length=50), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spaceships', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('model')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###