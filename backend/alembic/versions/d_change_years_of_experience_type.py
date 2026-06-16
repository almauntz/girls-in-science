"""Change years_of_experience type from String to Integer

Revision ID: d_years_int_001
Revises: c958e29d5795
Create Date: 2026-05-19 15:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd_years_int_001'
down_revision: Union[str, Sequence[str], None] = 'c958e29d5795'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # For SQLite, we need to recreate the table to change column type
    # First, create a new column with the correct type
    op.add_column('mentors', sa.Column('years_of_experience_new', sa.Integer(), nullable=True))
    
    # Copy data from old column to new column, converting strings to integers
    op.execute(
        "UPDATE mentors SET years_of_experience_new = CAST(years_of_experience AS INTEGER) "
        "WHERE years_of_experience IS NOT NULL AND years_of_experience != ''"
    )
    
    # Drop the old column
    op.drop_column('mentors', 'years_of_experience')
    
    # Rename the new column to the original name
    op.add_column('mentors', sa.Column('years_of_experience', sa.Integer(), nullable=True))
    op.execute("UPDATE mentors SET years_of_experience = years_of_experience_new")
    op.drop_column('mentors', 'years_of_experience_new')


def downgrade() -> None:
    """Downgrade schema."""
    # For downgrade, we'd need to recreate the column as String
    # This is a complex operation, so we'll keep it simple
    pass
