"""create posts table

Revision ID: 7bfd72f5b81c
Revises: 
Create Date: 2026-10-07 14:53:03.439421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bfd72f5b81c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(),nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
