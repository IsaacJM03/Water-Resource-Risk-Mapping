"""create alerts table

Revision ID: 8ce25c428b17
Revises: b0768f8bcecd
Create Date: 2026-01-23 16:25:49.976714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce25c428b17'
down_revision = 'b0768f8bcecd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("water_source_id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=True),

        sa.Column("level", sa.String(length=20), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),

        sa.ForeignKeyConstraint(
            ["water_source_id"], ["water_sources.id"], name="fk_alerts_water_source_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], name="fk_alerts_organization_id", ondelete="SET NULL"
        ),
    )

    op.create_index("ix_alerts_id", "alerts", ["id"])
    op.create_index("ix_alerts_acknowledged", "alerts", ["acknowledged"])
    op.create_index("ix_alerts_created_at", "alerts", ["created_at"])
    op.create_index("ix_alerts_water_source_id", "alerts", ["water_source_id"])
    op.create_index("ix_alerts_organization_id", "alerts", ["organization_id"])


def downgrade() -> None:
    op.drop_index("ix_alerts_organization_id", table_name="alerts")
    op.drop_index("ix_alerts_water_source_id", table_name="alerts")
    op.drop_index("ix_alerts_created_at", table_name="alerts")
    op.drop_index("ix_alerts_acknowledged", table_name="alerts")
    op.drop_index("ix_alerts_id", table_name="alerts")
    op.drop_table("alerts")