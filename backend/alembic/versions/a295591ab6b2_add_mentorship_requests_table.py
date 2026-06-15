"""add_mentorship_requests_table

Revision ID: a295591ab6b2
Revises: 706edfdc8cc9
Create Date: 2026-05-30 21:50:48.439860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a295591ab6b2'
down_revision: Union[str, Sequence[str], None] = '706edfdc8cc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop old student_applications table if it exists
    op.drop_table('student_applications', if_exists=True)
    
    # Create new mentorship_requests table
    op.create_table('mentorship_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_user_id', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED'), nullable=False, server_default='PENDING'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.id'], ),
    sa.ForeignKeyConstraint(['student_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.Index('ix_mentorship_requests_mentor_id', 'mentor_id'),
    sa.Index('ix_mentorship_requests_student_user_id', 'student_user_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('mentorship_requests')
    
    # Recreate student_applications if needed
    op.create_table('student_applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_user_id', sa.Integer(), nullable=False),
    sa.Column('mentor_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED'), nullable=False, server_default='PENDING'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentors.id'], ),
    sa.ForeignKeyConstraint(['student_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
