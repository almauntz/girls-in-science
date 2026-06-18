"""merge heads

Revision ID: a608a3829120
Revises: 123ec206e715, 1d83e1bc90d7, 37594ad9ce24, dca28dbd03a9, f14f0d6ad07c
Create Date: 2026-06-18 00:20:32.099666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a608a3829120'
down_revision: Union[str, Sequence[str], None] = ('123ec206e715', '1d83e1bc90d7', '37594ad9ce24', 'dca28dbd03a9', 'f14f0d6ad07c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
