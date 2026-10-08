"""add content column to posts table

Revision ID: c6f6b8d02a95
Revises: 7bfd72f5b81c
Create Date: 2026-10-08 08:24:52.276601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6f6b8d02a95'
down_revision: Union[str, Sequence[str], None] = '7bfd72f5b81c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
