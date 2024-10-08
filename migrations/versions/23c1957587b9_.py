"""empty message

Revision ID: 23c1957587b9
Revises: 6d5d1fdba230
Create Date: 2024-08-23 16:09:51.606736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23c1957587b9'
down_revision = '6d5d1fdba230'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('terrain', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('terrain')

    # ### end Alembic commands ###
