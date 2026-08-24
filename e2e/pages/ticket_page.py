from typing import Self

import allure
from playwright.sync_api import Page

from e2e.components import AuthPanel, TicketCreateForm

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

    @allure.step("Открыть главную страницу")
    def open(self) -> Self:
        self.page.goto(self.URL)

        return self