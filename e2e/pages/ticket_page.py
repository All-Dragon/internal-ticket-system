from typing import Self

import allure
from playwright.sync_api import Page

from e2e.components import (
    AuthPanel,
    TicketCreateForm,
    TicketEditModal,
    TicketTable,
    TicketDetailsModal,
    TicketDeleteConfirmModal,
    TicketFilters,
)


class TicketPage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page

        self.page_heading = page.get_by_role(
            "heading",
            name="Внутренние заявки",
            exact=True,
        )

        self.auth = AuthPanel(page)
        self.create_form = TicketCreateForm(page)
        self.ticket_table = TicketTable(page)
        self.edit_modal = TicketEditModal(page)
        self.details_modal = TicketDetailsModal(page)
        self.delete_modal = TicketDeleteConfirmModal(page)
        self.filters = TicketFilters(page)

    @allure.step("Открыть главную страницу")
    def open(self) -> Self:
        self.page.goto(self.URL)

        return self
