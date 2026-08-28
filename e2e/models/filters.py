from enum import StrEnum

class TicketSortBy(StrEnum):
    CREATED_AT = "created_at"
    PRIORITY = "priority"
    STATUS = "status"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"