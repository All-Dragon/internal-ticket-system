from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.enum import SortOrder, TicketPriority, TicketSortBy, TicketStatus


def capitalize_first_letter(value: str) -> str:
    value = value.strip()

    if not value:
        return value

    return value[0].upper() + value[1:]


class TicketBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = capitalize_first_letter(value)

        if len(value) < 3:
            raise ValueError("Заголовок должен содержать минимум 3 символа")

        return value

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = capitalize_first_letter(value)
        return value or None


class TicketCreate(TicketBase):
    priority: TicketPriority


class TicketUpdate(TicketBase):
    priority: TicketPriority


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(TicketBase):
    id: int
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketListParams(BaseModel):
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    search: str | None = Field(default=None, max_length=120)
    sort_by: TicketSortBy = TicketSortBy.created_at
    sort_order: SortOrder = SortOrder.desc
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    @field_validator("search")
    @classmethod
    def normalize_search(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()
        return value or None


class TicketListResponse(BaseModel):
    items: list[TicketRead]
    total: int
    page: int
    page_size: int
    pages: int
