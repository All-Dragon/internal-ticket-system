"""create tickets table

Revision ID: 9f2c1a8b7d6e
Revises:
Create Date: 2026-06-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f2c1a8b7d6e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "new",
                "in_progress",
                "done",
                name="ticket_status",
                native_enum=False,
                create_constraint=True,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.Enum(
                "low",
                "normal",
                "high",
                name="ticket_priority",
                native_enum=False,
                create_constraint=True,
                length=20,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "description IS NULL OR length(description) <= 1000",
            name="ck_tickets_description_max_length",
        ),
        sa.CheckConstraint("length(title) >= 3", name="ck_tickets_title_min_length"),
        sa.CheckConstraint("length(title) <= 120", name="ck_tickets_title_max_length"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tickets_created_at"), "tickets", ["created_at"], unique=False)
    op.create_index(op.f("ix_tickets_id"), "tickets", ["id"], unique=False)
    op.create_index(op.f("ix_tickets_priority"), "tickets", ["priority"], unique=False)
    op.create_index(op.f("ix_tickets_status"), "tickets", ["status"], unique=False)
    op.create_index(op.f("ix_tickets_title"), "tickets", ["title"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_tickets_title"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_status"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_priority"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_id"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_created_at"), table_name="tickets")
    op.drop_table("tickets")
