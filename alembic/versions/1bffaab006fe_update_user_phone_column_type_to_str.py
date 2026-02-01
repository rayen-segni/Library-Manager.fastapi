"""update user phone column type to str

Revision ID: 1bffaab006fe
Revises: e124bb92d79b
Create Date: 2026-02-01 14:06:18.971118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bffaab006fe'
down_revision = 'e124bb92d79b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users',
                    'phone', type_=sa.String(8),
                    existing_type=sa.Integer(),
                    nullable=False)


def downgrade():
    op.alter_column('users',
                    'phone', type_=sa.Integer(),
                    existing_type=sa.String(8),
                    nullable=True)
