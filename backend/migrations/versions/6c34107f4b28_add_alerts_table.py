"""add alerts table

Revision ID: 6c34107f4b28
Revises: d352735f6f75
Create Date: 2026-01-13 15:12:24.082464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c34107f4b28'
down_revision: Union[str, None] = 'a4e10a2b730e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('water_source_id', sa.Integer(), sa.ForeignKey('water_sources.id')),
        sa.Column('level', sa.String(length=20)),
        sa.Column('message', sa.String(length=255)),
        sa.Column('acknowledged', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('alerts')
