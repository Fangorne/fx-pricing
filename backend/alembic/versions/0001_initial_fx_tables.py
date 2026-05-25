"""initial_fx_tables

Revision ID: 0001
Revises:
Create Date: 2026-05-25

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fx_conventions",
        sa.Column("pair", sa.String(7), nullable=False),
        sa.Column("spot_lag", sa.Integer(), nullable=False),
        sa.Column("day_count", sa.String(20), nullable=False),
        sa.Column("roll_convention", sa.String(30), nullable=False),
        sa.Column("pip_precision", sa.Integer(), nullable=False),
        sa.Column("quotation_side", sa.String(10), nullable=False),
        sa.PrimaryKeyConstraint("pair"),
    )

    op.create_table(
        "market_calendars",
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("currency"),
    )

    op.create_table(
        "holidays",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("holiday_date", sa.Date(), nullable=False),
        sa.Column("description", sa.String(100), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(["currency"], ["market_calendars.currency"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_holidays_currency", "holidays", ["currency"])


def downgrade() -> None:
    op.drop_index("ix_holidays_currency", table_name="holidays")
    op.drop_table("holidays")
    op.drop_table("market_calendars")
    op.drop_table("fx_conventions")
