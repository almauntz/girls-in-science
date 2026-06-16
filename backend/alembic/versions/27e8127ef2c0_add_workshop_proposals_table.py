"""add workshop_proposals table

Revision ID: 27e8127ef2c0
Revises: cda93358c898
Create Date: 2026-05-29 18:09:23.720965
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27e8127ef2c0'
down_revision: Union[str, Sequence[str], None] = 'cda93358c898'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'workshop_proposals',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('location', sa.String, nullable=True),
        sa.Column('date', sa.DateTime, nullable=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('status', sa.String, nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('workshop_proposals')