"""Add profile_picture to Player and Scout models

Revision ID: fa565ac1a0d5
Revises: 870477c8377d
Create Date: 2024-07-23 01:29:42.562379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = 'fa565ac1a0d5'
down_revision: Union[str, None] = '870477c8377d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    # Check if the column exists in the 'players' table
    if 'profile_picture' not in [c['name'] for c in inspector.get_columns('players')]:
        op.add_column('players', sa.Column('profile_picture', sa.String(length=128), nullable=True))

    # Check if the column exists in the 'scouts' table
    if 'profile_picture' not in [c['name'] for c in inspector.get_columns('scouts')]:
        op.add_column('scouts', sa.Column('profile_picture', sa.String(length=128), nullable=True))

def downgrade() -> None:
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')
    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')
