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
        
        self.pagination = self.root.get_by_role(
            "navigation",
            name="Пагинация",
            exact=True
        )
        
        self.page_size_select = self.root.get_by_label(
            "На странице: ",
        )
        
        self.pagination = self.root.get_by_role(
            "navigation",
            name="Пагинация",
            exact=True,
        )

        self.page_size_select = self.root.get_by_role(
            "combobox",
            name="На странице:",
            exact=True,
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
        status: TicketStatus
    ) -> None:
        self.status_in_row(ticket_id).select_option(status.value)
    
    def _cell(
        self,
        ticket_id: int,
        ticket_column: _TicketColumn
    ) -> Locator:
        return self.row_by_id(ticket_id).locator("td").nth(ticket_column.value)