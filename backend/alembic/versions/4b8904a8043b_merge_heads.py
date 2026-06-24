"""merge heads

Revision ID: 4b8904a8043b
Revises: 65e581d150ce, 7876c3592572, a608a3829120
Create Date: 2026-06-24 15:47:04.105885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b8904a8043b'
down_revision: Union[str, Sequence[str], None] = ('65e581d150ce', '7876c3592572', 'a608a3829120')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if 'prijava' in tables:
        op.drop_table('prijava')
    if 'workshop' in tables:
        op.drop_table('workshop')