"""Initial migration

Revision ID: 542989e91443
Revises: 
Create Date: 2024-06-16 12:40:23.123423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '542989e91443'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'memes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_memes_id', 'memes', ['id'], unique=False)
    op.create_index('ix_memes_title', 'memes', ['title'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_memes_title', table_name='memes')
    op.drop_index('ix_memes_id', table_name='memes')
    op.drop_table('memes')
