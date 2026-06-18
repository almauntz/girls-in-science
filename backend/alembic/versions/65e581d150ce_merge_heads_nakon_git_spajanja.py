"""merge_heads_nakon_git_spajanja

Revision ID: 65e581d150ce
Revises: 1181ca1d788b, c448a07ef197
Create Date: 2026-06-17 12:44:00.054356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e581d150ce'
down_revision: Union[str, Sequence[str], None] = ('1181ca1d788b', 'c448a07ef197')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
