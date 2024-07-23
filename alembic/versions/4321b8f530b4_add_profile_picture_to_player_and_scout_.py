"""Add profile_picture to Player and Scout models (SQLite)

Revision ID: 4321b8f530b4
Revises: 3dba691f52de
Create Date: 2024-07-23 01:54:14.057196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4321b8f530b4'
down_revision: Union[str, None] = '3dba691f52de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add profile_picture column to Player table
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))

    # Add profile_picture column to Scout table
    with op.batch_alter_table('scout', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # Remove profile_picture column from Player table
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')

    # Remove profile_picture column from Scout table
    with op.batch_alter_table('scout', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')

