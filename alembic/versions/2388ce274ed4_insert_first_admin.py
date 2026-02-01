"""insert first admin

Revision ID: 2388ce274ed4
Revises: 3a40ba8c5c4c
Create Date: 2026-02-01 15:32:43.114202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2388ce274ed4'
down_revision = '3a40ba8c5c4c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
            INSERT INTO users (cin, role, full_name, email, age, password, phone)
            VALUES ('12345678', 'admin', 'Mohamed Rayen Segni', 'rayen@mail.com', 19, '$2b$12$ouSN3uYL9IWlDCRcs0RY/u2ELdaFDCd7T4gcIkPn/cztippmfNcO2', '22841069')
            """)


def downgrade():
    op.execute("""
            DELETE FROM users WHERE cin='12345678'
            """)
