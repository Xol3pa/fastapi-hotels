"""emai is unique

Revision ID: d4586da5f76c
Revises: 28c6598a7902
Create Date: 2025-05-20 18:26:07.600434

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d4586da5f76c"
down_revision: Union[str, None] = "28c6598a7902"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
