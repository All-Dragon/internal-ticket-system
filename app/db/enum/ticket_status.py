import enum

from sqlalchemy import Enum as SQLEnum


class TicketStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


def ticket_status_enum() -> SQLEnum:
    return SQLEnum(
        TicketStatus,
        name="ticket_status",
        values_callable=lambda values: [value.value for value in values],
        native_enum=False,
        create_constraint=True,
        length=20,
    )
