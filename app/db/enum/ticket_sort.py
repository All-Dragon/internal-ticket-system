import enum


class TicketSortBy(str, enum.Enum):
    created_at = "created_at"
    priority = "priority"
    status = "status"


class SortOrder(str, enum.Enum):
    asc = "asc"
    desc = "desc"