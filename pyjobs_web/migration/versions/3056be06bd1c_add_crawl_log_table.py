"""Add crawl_log table

Revision ID: 3056be06bd1c
Revises: 3e1b639a5568
Create Date: 2016-01-14 17:30:35.905916

"""

# revision identifiers, used by Alembic.
revision = '3056be06bd1c'
down_revision = '3e1b639a5568'

import sqlalchemy as sa
from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crawl_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=64), nullable=True),
    sa.Column('message', sa.String(length=1024), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crawl_log')
    ### end Alembic commands ###
