"""merge_branch_konflikt

Revision ID: 37594ad9ce24
Revises: 6562f9b20ac7, f4bf505fb176
Create Date: 2026-06-02 22:51:34.020403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37594ad9ce24'
down_revision: Union[str, Sequence[str], None] = ('6562f9b20ac7', 'f4bf505fb176')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
