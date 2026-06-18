"""add status and rejection_reason to mentors

Revision ID: c448a07ef197
Revises: dca723a6d58f
Create Date: 2026-06-16 10:52:10.776785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c448a07ef197'
down_revision: Union[str, Sequence[str], None] = 'dca723a6d58f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('mentors', sa.Column('status', sa.VARCHAR(), nullable=False, server_default='PENDING'))
    op.add_column('mentors', sa.Column('rejection_reason', sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column('mentors', 'rejection_reason')
    op.drop_column('mentors', 'status')