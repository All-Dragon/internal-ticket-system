from playwright.sync_api import Page

from e2e.models.ticket import TicketPriority, TicketStatus
from e2e.models.filters import SortOrder, TicketSortBy

class TicketFilters:
    def __init__(self, page: Page):
        self.root = page.get_by_role(
            "region",
            name="Фильтры заявок",
            exact=True,
        )

        self.search_field = self.root.get_by_role(
            "searchbox",
            name="Поиск",
            exact=True,
        )

        self.status_field = self.root.get_by_role(
            "combobox",
            name="Статус",
            exact=True,
        )

        self.priority_field = self.root.get_by_role(
            "combobox",
            name="Приоритет",
            exact=True,
        )

        self.sort_by_field = self.root.get_by_role(
            "combobox",
            name="Сортировать по",
            exact=True,
        )

        self.sort_order_field = self.root.get_by_role(
            "combobox",
            name="Направление сортировки",
            exact=True,
        )

        self.reset_button = self.root.get_by_role(
            "button",
            name="Сбросить фильтры",
            exact=True,
        )

    def search(self, query: str) -> None:
        self.search_field.fill(query)

    def filter_by_status(
        self,
        status: TicketStatus | None,
    ) -> None:
        value = status.value if status is not None else ""
        self.status_field.select_option(value)

    def filter_by_priority(
        self,
        priority: TicketPriority | None,
    ) -> None:
        value = priority.value if priority is not None else ""
        self.priority_field.select_option(value)

    def sort_by(
        self,
        sort_by: TicketSortBy,
    ) -> None:
        value = sort_by.value if sort_by is not None else ""
        self.sort_by_field.select_option(value)

    def set_sort_order(
        self,
        sort_order: SortOrder,
    ) -> None:
        value = sort_order.value if sort_order is not None else ""
        self.sort_order_field.select_option(value)

    def reset(self) -> None:
        self.reset_button.click()
