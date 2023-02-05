"""create phone number column for user table

Revision ID: cf5a608893f1
Revises: 8d41adf7da6e
Create Date: 2023-02-05 16:42:28.471693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf5a608893f1'
down_revision = '8d41adf7da6e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_number')
