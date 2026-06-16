"""merge multiple heads

Revision ID: 706edfdc8cc9
Revises: 188d606ce5a2, b7f22ec7a4fe, d_years_int_001
Create Date: 2026-05-19 21:55:06.240547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '706edfdc8cc9'
down_revision: Union[str, Sequence[str], None] = ('188d606ce5a2', 'b7f22ec7a4fe', 'd_years_int_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
