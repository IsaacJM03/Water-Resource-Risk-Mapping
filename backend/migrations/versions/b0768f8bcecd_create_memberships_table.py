"""create memberships table

Revision ID: b0768f8bcecd
Revises: 02a71457d284
Create Date: 2026-01-20 15:41:05.432637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0768f8bcecd'
down_revision = '02a71457d284'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=True),

        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_memberships_user_id", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_memberships_organization_id",
            ondelete="CASCADE",
        ),
    )

    op.create_index("ix_memberships_id", "memberships", ["id"])
    op.create_index("ix_memberships_user_id", "memberships", ["user_id"])
    op.create_index("ix_memberships_organization_id", "memberships", ["organization_id"])
    op.create_index(
        "uq_memberships_user_org",
        "memberships",
        ["user_id", "organization_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_memberships_user_org", table_name="memberships")
    op.drop_index("ix_memberships_organization_id", table_name="memberships")
    op.drop_index("ix_memberships_user_id", table_name="memberships")
    op.drop_index("ix_memberships_id", table_name="memberships")
    op.drop_table("memberships")