"""empty message

Revision ID: ffb338ffe1f7
Revises: 88cd298d5e68
Create Date: 2016-08-12 17:00:53.090006

"""

# revision identifiers, used by Alembic.
revision = 'ffb338ffe1f7'
down_revision = '88cd298d5e68'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('homework', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('homework', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    ### end Alembic commands ###
