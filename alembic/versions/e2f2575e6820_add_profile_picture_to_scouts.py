"""Add profile_picture to scouts

Revision ID: e2f2575e6820
Revises: 4321b8f530b4
Create Date: 2024-07-23 02:03:15.817161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2f2575e6820'
down_revision: Union[str, None] = '4321b8f530b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add column to scouts table
    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=128), nullable=True))


def downgrade() -> None:
    # Drop column from scouts table
    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.drop_column('profile_picture')
