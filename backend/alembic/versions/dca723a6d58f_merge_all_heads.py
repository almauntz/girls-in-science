"""merge all heads

Revision ID: dca723a6d58f
Revises: 123ec206e715, 1d83e1bc90d7, 37594ad9ce24, dca28dbd03a9, f14f0d6ad07c
Create Date: 2026-06-16 09:43:54.746613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dca723a6d58f'
down_revision: Union[str, Sequence[str], None] = ('123ec206e715', '1d83e1bc90d7', '37594ad9ce24', 'dca28dbd03a9', 'f14f0d6ad07c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
