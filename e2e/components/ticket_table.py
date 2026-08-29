from enum import IntEnum

from playwright.sync_api import Locator, Page

from e2e.models.ticket import TicketStatus


class _TicketColumn(IntEnum):
    ID = 0
    TITLE = 1
    DESCRIPTION = 2
    STATUS = 3
    PRIORITY = 4


class TicketTable:
    def __init__(self, page: Page):
        self.page = page

        self.root = page.get_by_role(
            "region",
            name="Список заявок",
            exact=True,
        )

        self.table = self.root.get_by_role(
            "table",
            name="Список заявок",
            exact=True,
        )

        self.rows = self.table.locator("tbody").get_by_role("row")

        self.pagination = self.root.get_by_role(
            "navigation",
            name="Пагинация",
            exact=True,
        )

        self.previous_page_button = self.pagination.get_by_role(
            "button",
            name="Назад",
            exact=True,
        )

        self.next_page_button = self.pagination.get_by_role(
            "button",
            name="Далее",
            exact=True,
        )

        self.page_size_field = self.root.get_by_role(
            "combobox",
            name="На странице:",
            exact=True,
        )

        self.pagination_summary = self.root.locator(
            '[aria-live="polite"]'
        )

        self.empty_tickets_state = page.get_by_role(
            "status",
        ).filter(
            has=page.get_by_role(
                "heading",
                name="Заявки не найдены",
                exact=True,
            )
        )

    def row_by_id(self, ticket_id: int) -> Locator:
        return self.table.get_by_role("row").filter(
            has=self.page.get_by_text(
                f"#{ticket_id}",
                exact=True,
            )
        )

    def view_button(self, ticket_id: int) -> Locator:
        return self.root.get_by_role(
            "button",
            name=f"Посмотреть заявку #{ticket_id}",
            exact=True,
        )

    def edit_button(self, ticket_id: int) -> Locator:
        return self.root.get_by_role(
            "button",
            name=f"Редактировать заявку #{ticket_id}",
            exact=True,
        )

    def delete_button(self, ticket_id: int) -> Locator:
        return self.root.get_by_role(
            "button",
            name=f"Удалить заявку #{ticket_id}",
            exact=True,
        )

    def title_in_row(self, ticket_id: int) -> Locator:
        return self._cell(ticket_id, _TicketColumn.TITLE)

    def description_in_row(self, ticket_id: int) -> Locator:
        return self._cell(ticket_id, _TicketColumn.DESCRIPTION)

    def priority_in_row(self, ticket_id: int) -> Locator:
        return self._cell(ticket_id, _TicketColumn.PRIORITY)

    def status_in_row(self, ticket_id: int) -> Locator:
        return self.row_by_id(ticket_id).get_by_role(
            "combobox",
            name=f"Статус заявки #{ticket_id}",
            exact=True,
        )

    def change_status(
        self,
        ticket_id: int,
        status: TicketStatus,
    ) -> None:
        self.status_in_row(ticket_id).select_option(status.value)

    def page_button(
        self,
        page_number: int,
    ) -> Locator:
        return self.pagination.get_by_role(
            "button",
            name=str(page_number),
            exact=True,
        )

    def go_to_page(
        self,
        page_number: int,
    ) -> None:
        self.page_button(page_number).click()

    def go_to_next_page(self) -> None:
        self.next_page_button.click()

    def go_to_previous_page(self) -> None:
        self.previous_page_button.click()

    def set_page_size(
        self,
        page_size: int,
    ) -> None:
        self.page_size_field.select_option(
            str(page_size),
        )

    def _cell(
        self,
        ticket_id: int,
        ticket_column: _TicketColumn,
    ) -> Locator:
        return self.row_by_id(ticket_id).locator("td").nth(ticket_column.value)
