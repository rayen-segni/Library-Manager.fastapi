"""create loans tables

Revision ID: 2adff2e19034
Revises: 6ebad8c1e2af
Create Date: 2026-01-30 20:39:36.507352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2adff2e19034'
down_revision = '6ebad8c1e2af'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("loans",
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('client_id', sa.Integer(), nullable=False),
                    sa.Column('book_id', sa.Integer(), nullable=False),
                    sa.Column('start_date', sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False),
                    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column('retrieved', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(["client_id"], ["users.id"], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete='CASCADE')
                    )


def downgrade():
    op.drop_table("loans")

