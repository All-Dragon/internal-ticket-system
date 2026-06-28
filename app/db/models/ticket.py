from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.enum import (
    TicketPriority,
    TicketStatus,
    ticket_priority_enum,
    ticket_status_enum,
)
from app.db.models.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        CheckConstraint("length(title) >= 3", name="ck_tickets_title_min_length"),
        CheckConstraint("length(title) <= 120", name="ck_tickets_title_max_length"),
        CheckConstraint(
            "description IS NULL OR length(description) <= 1000",
            name="ck_tickets_description_max_length",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[TicketStatus] = mapped_column(
        ticket_status_enum(),
        default=TicketStatus.new,
        nullable=False,
        index=True,
    )

    priority: Mapped[TicketPriority] = mapped_column(
        ticket_priority_enum(),
        default=TicketPriority.normal,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
