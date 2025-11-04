"""Add role column to users

Revision ID: afcfeed46e3f
Revises: dcd16f90fbbe
Create Date: 2025-11-04 18:04:49.061966
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "afcfeed46e3f"
down_revision: Union[str, Sequence[str], None] = "dcd16f90fbbe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


userrole_enum = sa.Enum("ADMIN", "REGULAR", name="userrole")


def upgrade() -> None:
    """Upgrade schema."""
    userrole_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "users",
        sa.Column(
            "role",
            userrole_enum,
            server_default="REGULAR",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
    userrole_enum.drop(op.get_bind(), checkfirst=True)
