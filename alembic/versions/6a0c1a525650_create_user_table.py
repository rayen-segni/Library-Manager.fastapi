"""create user table

Revision ID: 6a0c1a525650
Revises: 
Create Date: 2026-01-30 20:31:37.338945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a0c1a525650'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('cin', sa.String(), nullable=False),
                    sa.Column('role', sa.String(), server_default='user', nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), unique=True, nullable=False),
                    sa.Column('age', sa.Integer(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"), nullable=False)
                    )


def downgrade():
    op.drop_table("users")
