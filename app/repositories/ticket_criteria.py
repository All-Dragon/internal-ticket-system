from dataclasses import dataclass

from app.db.enum import SortOrder, TicketPriority, TicketSortBy, TicketStatus


@dataclass(frozen=True)
class TicketListCriteria:
    status: TicketStatus | None
    priority: TicketPriority | None
    search: str | None
    sort_by: TicketSortBy
    sort_order: SortOrder
    offset: int
    limit: int