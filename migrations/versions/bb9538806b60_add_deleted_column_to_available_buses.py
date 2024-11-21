"""Add deleted column to available_buses

Revision ID: bb9538806b60
Revises: 1e0ebcc128ef
Create Date: 2024-10-30 17:53:29.996976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb9538806b60'
down_revision = '1e0ebcc128ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('available_buses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('available_buses', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    # ### end Alembic commands ###
