"""add collection name column to sources table

Revision ID: 42b696643c11
Revises: 47ed4ef83f44
Create Date: 2023-01-16 22:17:37.732258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "42b696643c11"
down_revision = "47ed4ef83f44"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("collection_name", sa.String))


def downgrade() -> None:
    op.drop_column("sources", "collection_name")
