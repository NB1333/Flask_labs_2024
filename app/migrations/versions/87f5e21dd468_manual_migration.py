"""Manual migration

Revision ID: 87f5e21dd468
Revises: 413fac1e130e
Create Date: 2024-05-16 00:57:30.787553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87f5e21dd468'
down_revision = '413fac1e130e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('uah_balance', sa.Float(), nullable=False, default=0.0))
    op.add_column('user', sa.Column('usd_balance', sa.Float(), nullable=False, default=0.0))
    


def downgrade():
    op.drop_column('user', 'uah_balance')
    op.drop_column('user', 'usd_balance')
