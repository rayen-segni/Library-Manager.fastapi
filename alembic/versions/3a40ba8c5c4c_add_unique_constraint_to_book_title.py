"""add unique constraint to book title

Revision ID: 3a40ba8c5c4c
Revises: 1bffaab006fe
Create Date: 2026-02-01 14:39:17.632981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a40ba8c5c4c'
down_revision = '1bffaab006fe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("uq_title",
                                "books",
                                ['title'])


def downgrade():
    op.drop_constraint("uq_title", "books", type_="unique")
