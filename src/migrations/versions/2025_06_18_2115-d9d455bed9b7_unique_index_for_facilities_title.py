"""Unique index for facilities title

Revision ID: d9d455bed9b7
Revises: 171f8985ce9c
Create Date: 2025-06-18 21:15:04.367887

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d9d455bed9b7"
down_revision: Union[str, None] = "171f8985ce9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "ix_facilities_title_lower",
        "facilities",
        [sa.literal_column("lower(title)")],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_facilities_title_lower", table_name="facilities")
