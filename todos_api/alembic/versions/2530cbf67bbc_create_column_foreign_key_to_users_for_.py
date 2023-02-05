"""create column/foreign_key to users for address_id

Revision ID: 2530cbf67bbc
Revises: 1483062d1f1d
Create Date: 2023-02-05 17:06:12.798588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2530cbf67bbc'
down_revision = '1483062d1f1d'
branch_labels = None
depends_on = '1483062d1f1d'


def upgrade():
    op.add_column('address_id', sa.Integer(), nullable=True)
    op.create_foreign_key("fk_user_address", source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint("fk_user_address", table_name='users')
    op.drop_column('users', 'address_id')
