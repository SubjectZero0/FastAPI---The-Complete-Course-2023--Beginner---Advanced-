"""create address table

Revision ID: 1483062d1f1d
Revises: cf5a608893f1
Create Date: 2023-02-05 16:52:33.328932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1483062d1f1d'
down_revision = 'cf5a608893f1'
branch_labels = None
depends_on = 'cf5a608893f1'


def upgrade():
    op.create_table('address',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),

                    sa.Column('primary_address', sa.String(), nullable=False),

                    sa.Column('secondary_address',
                              sa.String(), nullable=True),

                    sa.Column('city',
                              sa.String(), nullable=False),

                    sa.Column('state',
                              sa.String(), nullable=False),

                    sa.Column('country',
                              sa.String(), nullable=False),

                    sa.Column('postal_code',
                              sa.String(), nullable=False),

                    )


def downgrade():
    op.drop_table('address')
