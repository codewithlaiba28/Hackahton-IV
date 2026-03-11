"""Initial schema - users, chapters, quizzes, progress

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-01-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types (skip if exists - for Neon DB compatibility)
    # Check if enum already exists
    conn = op.get_bind()
    enum_exists = conn.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'usertier'")
    ).first()
    
    if not enum_exists:
        user_tier = sa.Enum('FREE', 'PREMIUM', 'PRO', name='usertier')
        user_tier.create(op.get_bind())
    else:
        # Use existing enum
        user_tier = sa.Enum('FREE', 'PREMIUM', 'PRO', name='usertier', create_type=False)

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('api_key', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('tier', user_tier, nullable=False, default='FREE'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_api_key'), 'users', ['api_key'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create chapters table
    op.create_table('chapters',
        sa.Column('id', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('estimated_read_min', sa.Integer(), nullable=False),
        sa.Column('is_free', sa.Boolean(), nullable=False, default=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('prev_chapter_id', sa.String(length=20), nullable=True),
        sa.Column('next_chapter_id', sa.String(length=20), nullable=True),
        sa.Column('r2_content_key', sa.String(length=255), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['next_chapter_id'], ['chapters.id'], ),
        sa.ForeignKeyConstraint(['prev_chapter_id'], ['chapters.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapters_sequence_order'), 'chapters', ['sequence_order'], unique=True)

    # Create quiz_questions table
    op.create_table('quiz_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=20), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(length=20), nullable=False),
        sa.Column('options', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('correct_answer', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create chapter_progress table
    op.create_table('chapter_progress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, default='not_started'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'chapter_id', name='uq_user_chapter_progress')
    )

    # Create daily_activity table
    op.create_table('daily_activity',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'activity_date', name='uq_user_daily_activity')
    )

    # Create quiz_attempts table
    op.create_table('quiz_attempts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=20), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('total', sa.Integer(), nullable=False),
        sa.Column('percentage', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('quiz_attempts')
    op.drop_table('daily_activity')
    op.drop_table('chapter_progress')
    op.drop_table('quiz_questions')
    op.drop_table('chapters')
    op.drop_table('users')

    # Drop enum type
    user_tier = sa.Enum('FREE', 'PREMIUM', 'PRO', name='usertier')
    user_tier.drop(op.get_bind())
