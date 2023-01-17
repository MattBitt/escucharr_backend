"""create test table to test alembic

Revision ID: 47ed4ef83f44
Revises: 
Create Date: 2023-01-16 22:03:13.059152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "47ed4ef83f44"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "testing_alembic",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table("testing_alembic")
