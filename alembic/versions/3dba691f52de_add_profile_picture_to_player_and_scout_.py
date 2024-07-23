"""Add profile_picture to Player and Scout models (SQLite)

Revision ID: 3dba691f52de
Revises: fa565ac1a0d5
Create Date: 2024-07-23 01:41:02.995556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dba691f52de'
down_revision: Union[str, None] = 'fa565ac1a0d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('profile_picture', sa.String(length=128), nullable=True))
    op.add_column('scouts', sa.Column('profile_picture', sa.String(length=128), nullable=True))

    # SQLite does not support ALTER COLUMN directly, so we need to use a workaround:
    # 1. Create a new table with the updated schema.
    op.create_table(
        'players_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=False),
        sa.Column('profile_picture', sa.String(length=128), nullable=True),
        sa.Column('date_of_birth', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Copy data from the old table to the new table.
    op.execute('INSERT INTO players_new (id, name, profile_picture, date_of_birth) SELECT id, name, profile_picture, date_of_birth FROM players')

    # 3. Drop the old table and rename the new table.
    op.drop_table('players')
    op.rename_table('players_new', 'players')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scouts', 'profile_picture')
    op.drop_column('players', 'profile_picture')

    # SQLite does not support ALTER COLUMN directly, so we need to use a workaround:
    # 1. Create a new table with the original schema.
    op.create_table(
        'players_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=False),
        sa.Column('date_of_birth', sa.String(length=60), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. Copy data from the new table to the old table.
    op.execute('INSERT INTO players_old (id, name, date_of_birth) SELECT id, name, date_of_birth FROM players')

    # 3. Drop the new table and rename the old table.
    op.drop_table('players')
    op.rename_table('players_old', 'players')

    # ### end Alembic commands ###