"""add file_path column

Revision ID: 28e21f2c96b7
Revises: a02d6d4ceea9
Create Date: 2025-01-02 08:28:44.317136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28e21f2c96b7'
down_revision = 'a02d6d4ceea9'
branch_labels = None
depends_on = None

_column = 'file_path'


def upgrade():
    op.add_column('ckanext_metadata', sa.Column(_column, sa.UnicodeText))


def downgrade():
    op.drop_column('ckanext_metadata', _column)
