"""empty message

Revision ID: 4f366e8c8cc1
Revises: c91b3f952b8c
Create Date: 2016-09-26 17:42:55.191110

"""

# revision identifiers, used by Alembic.
revision = '4f366e8c8cc1'
down_revision = 'c91b3f952b8c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test', 'timeout',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test', 'timeout',
               existing_type=sa.INTEGER(),
               nullable=False)
    ### end Alembic commands ###
