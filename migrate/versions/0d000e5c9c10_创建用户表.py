"""创建用户表

Revision ID: 0d000e5c9c10
Revises:
Create Date: 2025-09-28 21:10:53.672083

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0d000e5c9c10"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 创建用户名
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("email", sa.String()),
        sa.Column("phone", sa.String()),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )

    # 创建索引, 加快查询
    op.create_index(
        op.f("ix_user_username"),
        "user",
        ["username"],
        unique=True,
        if_not_exists=True,
    )
    op.create_index(
        op.f("ix_user_phone"),
        "user",
        ["phone"],
        unique=True,
        if_not_exists=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_user_phone"), table_name="user", if_exists=True)
    op.drop_index(op.f("ix_user_username"), table_name="user", if_exists=True)

    op.drop_table("user", if_exists=True)
