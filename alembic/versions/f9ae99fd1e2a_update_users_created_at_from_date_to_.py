"""update users created_at from date to datetime

Revision ID: f9ae99fd1e2a
Revises: 317db015aea4
Create Date: 2022-12-01 17:47:29.472540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ae99fd1e2a'
down_revision = '317db015aea4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
