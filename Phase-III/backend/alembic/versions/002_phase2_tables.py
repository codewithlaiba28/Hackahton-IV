"""Phase 2 tables - LLM usage tracking and hybrid features

Revision ID: 002
Revises: 001
Create Date: 2026-03-11

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create Phase 2 tables for hybrid intelligence features."""
    
    # 1. LLM Usage Tracking Table
    op.create_table(
        'llm_usage',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feature_name', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('input_tokens', sa.Integer(), nullable=False),
        sa.Column('output_tokens', sa.Integer(), nullable=False),
        sa.Column('cost_usd', sa.Numeric(precision=10, scale=6), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_llm_usage_user_id', 'llm_usage', ['user_id'], unique=False)
    op.create_index('ix_llm_usage_feature_name', 'llm_usage', ['feature_name'], unique=False)
    op.create_index('ix_llm_usage_created_at', 'llm_usage', ['created_at'], unique=False)
    
    # 2. Adaptive Recommendations Table
    op.create_table(
        'adaptive_recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('recommended_chapters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('weak_areas', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('strengths', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('overall_assessment', sa.Text(), nullable=False),
        sa.Column('suggested_daily_minutes', sa.Integer(), nullable=True),
        sa.Column('llm_usage_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['llm_usage_id'], ['llm_usage.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_adaptive_recommendations_user_id', 'adaptive_recommendations', ['user_id'], unique=False)
    op.create_index('ix_adaptive_recommendations_created_at', 'adaptive_recommendations', ['created_at'], unique=False)
    # Composite index for efficient "latest recommendation" queries
    op.create_index(
        'ix_adaptive_recommendations_user_created',
        'adaptive_recommendations',
        ['user_id', sa.text('created_at DESC')]
    )
    
    # 3. Assessment Questions Table
    op.create_table(
        'assessment_questions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=20), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('model_answer_criteria', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_assessment_questions_chapter_id', 'assessment_questions', ['chapter_id'], unique=False)
    
    # 4. Assessment Results Table
    op.create_table(
        'assessment_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('chapter_id', sa.String(length=20), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('grade', sa.String(length=2), nullable=False),
        sa.Column('correct_concepts', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('missing_concepts', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=False),
        sa.Column('improvement_suggestions', sa.Text(), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False),
        sa.Column('llm_usage_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('score >= 0 AND score <= 100', name='check_assessment_score_range'),
        sa.CheckConstraint('word_count >= 0', name='check_word_count_positive'),
        sa.ForeignKeyConstraint(['llm_usage_id'], ['llm_usage.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['assessment_questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_assessment_results_user_id', 'assessment_results', ['user_id'], unique=False)
    op.create_index('ix_assessment_results_chapter_id', 'assessment_results', ['chapter_id'], unique=False)
    # Composite index for efficient user+chapter queries
    op.create_index(
        'ix_assessment_results_user_chapter',
        'assessment_results',
        ['user_id', 'chapter_id']
    )


def downgrade() -> None:
    """Remove Phase 2 tables - Phase 1 tables remain untouched."""
    
    # Drop in reverse order of creation (respecting foreign keys)
    op.drop_index('ix_assessment_results_user_chapter', table_name='assessment_results')
    op.drop_index('ix_assessment_results_chapter_id', table_name='assessment_results')
    op.drop_index('ix_assessment_results_user_id', table_name='assessment_results')
    op.drop_table('assessment_results')
    
    op.drop_index('ix_assessment_questions_chapter_id', table_name='assessment_questions')
    op.drop_table('assessment_questions')
    
    op.drop_index('ix_adaptive_recommendations_user_created', table_name='adaptive_recommendations')
    op.drop_index('ix_adaptive_recommendations_created_at', table_name='adaptive_recommendations')
    op.drop_index('ix_adaptive_recommendations_user_id', table_name='adaptive_recommendations')
    op.drop_table('adaptive_recommendations')
    
    op.drop_index('ix_llm_usage_created_at', table_name='llm_usage')
    op.drop_index('ix_llm_usage_feature_name', table_name='llm_usage')
    op.drop_index('ix_llm_usage_user_id', table_name='llm_usage')
    op.drop_table('llm_usage')
