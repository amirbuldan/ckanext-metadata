"""create metadata table

Revision ID: a02d6d4ceea9
Revises: 
Create Date: 2024-12-16 08:26:39.152941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a02d6d4ceea9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    engine = op.get_bind()
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()

    if "ckanext_metadata" not in tables:
        op.create_table(
            "ckanext_metadata",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("organization_id", sa.UnicodeText, default=""),
            sa.Column("title", sa.UnicodeText, default=""),
            sa.Column("desc", sa.UnicodeText, default=""),
            sa.Column("author", sa.UnicodeText, default=""),
            sa.Column("created", sa.DateTime),
            sa.Column("modified", sa.DateTime)
        )


def downgrade():
    op.drop_table("ckanext_metadata")
