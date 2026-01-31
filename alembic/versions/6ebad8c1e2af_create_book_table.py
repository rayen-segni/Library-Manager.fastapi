"""create book table

Revision ID: 6ebad8c1e2af
Revises: 6a0c1a525650
Create Date: 2026-01-30 20:36:58.750397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ebad8c1e2af'
down_revision = '6a0c1a525650'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("books",
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('copies', sa.Integer(), server_default='0', nullable=False),
                    sa.Column('added_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False)
                    )


def downgrade():
    op.drop_table("books")

