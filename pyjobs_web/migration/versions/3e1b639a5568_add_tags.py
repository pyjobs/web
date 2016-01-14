"""add tags

Revision ID: 3e1b639a5568
Revises: 454ccccb5769
Create Date: 2015-10-30 16:55:04.892060

"""

# revision identifiers, used by Alembic.
revision = '3e1b639a5568'
down_revision = '454ccccb5769'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('jobs', sa.Column('tags', sa.Text(), nullable=True, default=''))


def downgrade():
    op.drop_column('jobs', 'tags')
