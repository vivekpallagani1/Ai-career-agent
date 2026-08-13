"""Initial migration: users, profiles, jobs, resumes, applications

Revision ID: 001
Revises: 
Create Date: 2026-08-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='candidate'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_users_email', 'email'),
    )

    op.create_table(
        'candidate_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('bio', sa.Text()),
        sa.Column('profile_completeness', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('target_roles', sa.Text()),
        sa.Column('preferred_locations', sa.Text()),
        sa.Column('min_salary', sa.Integer()),
        sa.Column('max_salary', sa.Integer()),
        sa.Column('experience_level', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_candidate_profiles_user_id', 'user_id'),
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(255), nullable=False, unique=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('company', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255)),
        sa.Column('salary_min', sa.Integer()),
        sa.Column('salary_max', sa.Integer()),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('source', sa.String(100)),
        sa.Column('employment_type', sa.String(50)),
        sa.Column('seniority_level', sa.String(50)),
        sa.Column('parsed_data', sa.Text()),
        sa.Column('posted_at', sa.String(50)),
        sa.Column('fraud_score', sa.Integer(), nullable=False, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_jobs_external_id', 'external_id'),
    )

    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('extracted_data', sa.Text()),
        sa.Column('created_at', sa.String(50), nullable=False, server_default='2026-08-13T00:00:00Z'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_resumes_user_id', 'user_id'),
    )

    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='saved'),
        sa.Column('resume_used', sa.Integer()),
        sa.Column('match_score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.String(50)),
        sa.Column('updated_at', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_applications_user_id', 'user_id'),
        sa.Index('ix_applications_job_id', 'job_id'),
    )


def downgrade() -> None:
    op.drop_table('applications')
    op.drop_table('resumes')
    op.drop_table('jobs')
    op.drop_table('candidate_profiles')
    op.drop_table('users')
