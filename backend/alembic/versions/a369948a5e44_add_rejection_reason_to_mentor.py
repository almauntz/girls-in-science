"""add rejection_reason to mentor
Revision ID: a369948a5e44
Revises: 706edfdc8cc9
Create Date: 2026-05-31 20:43:34.795518
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a369948a5e44'
down_revision: Union[str, Sequence[str], None] = '706edfdc8cc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('mentors', sa.Column('rejection_reason', sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column('mentors', 'rejection_reason')