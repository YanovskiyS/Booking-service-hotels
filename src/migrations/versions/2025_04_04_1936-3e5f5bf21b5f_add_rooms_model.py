"""add rooms model

Revision ID: 3e5f5bf21b5f
Revises: 94065c80ed59
Create Date: 2025-04-04 19:36:49.435478

"""

from typing import Sequence, Union




# revision identifiers, used by Alembic.
revision: str = "3e5f5bf21b5f"
down_revision: Union[str, None] = "94065c80ed59"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    pass



def downgrade() -> None:
    """Downgrade schema."""

    pass

