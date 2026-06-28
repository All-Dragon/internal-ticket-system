import enum

from sqlalchemy import Enum as SQLEnum


class TicketPriority(str, enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"


def ticket_priority_enum() -> SQLEnum:
    return SQLEnum(
        TicketPriority,
        name="ticket_priority",
        values_callable=lambda values: [value.value for value in values],
        native_enum=False,
        create_constraint=True,
        length=20,
    )