"""create practice entries table

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "practice_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("practiced_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_practice_entries_practiced_at",
        "practice_entries",
        ["practiced_at"],
    )


def downgrade():
    op.drop_index("ix_practice_entries_practiced_at", table_name="practice_entries")
    op.drop_table("practice_entries")
