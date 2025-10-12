"""创建用户权限表

Revision ID: 6ccce31b2bcd
Revises: 0d000e5c9c10
Create Date: 2025-09-28 21:11:32.404306

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6ccce31b2bcd"
down_revision: Union[str, Sequence[str], None] = "0d000e5c9c10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_permission",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("permission", sa.Integer(), nullable=False),
        if_not_exists=True,
    )
    op.create_index(
        op.f("ix_user_permission_user_id"),
        "user_permission",
        ["user_id"],
        unique=False,
        if_not_exists=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_user_permission_user_id"),
        table_name="user_permission",
        if_exists=True,
    )

    op.drop_table("user_permission", if_exists=True)
