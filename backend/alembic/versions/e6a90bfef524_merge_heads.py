"""merge heads

Revision ID: e6a90bfef524
Revises: a295591ab6b2, a369948a5e44
Create Date: 2026-06-01 14:06:33.752282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6a90bfef524'
down_revision: Union[str, Sequence[str], None] = ('a295591ab6b2', 'a369948a5e44')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
