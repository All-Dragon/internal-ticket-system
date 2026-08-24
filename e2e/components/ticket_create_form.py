from typing import Self

import allure
from playwright.sync_api import Page


class TicketCreateForm:
    def __init__(self, page: Page):
        self.root = page.get_by_role(
            "region",
            name="Создать заявку",
        )

        self.title_input = self.root.get_by_role(
            "textbox",
            name="Заголовок",
            exact=True,
        )

        self.description_input = self.root.get_by_role(
            "textbox",
            name="Описание",
            exact=True,
        )

        self.priority_select = self.root.get_by_role(
            "combobox",
            name="Приоритет",
            exact=True,
        )

        self.submit_button = self.root.get_by_role(
            "button",
            name="+ Создать заявку",
            exact=True,
        )

        self.created_dialog = page.get_by_role(
            "dialog",
            name="Заявка создана",
        )

        self.created_dialog_close_button = self.created_dialog.get_by_role(
            "button",
            name="Понятно",
            exact=True,
        )

        self.title_error = self.root.locator("#ticket-title-error")

        self.description_error = self.root.locator(
            "#ticket-description-error"
        )

    @allure.step("Создать заявку: {title}")
    def create(
        self,
        title: str,
        description: str,
        priority: str,
    ) -> Self:
        self.title_input.fill(title)
        self.description_input.fill(description)
        self.priority_select.select_option(priority)
        self.submit_button.click()

        return self

    @allure.step("Закрыть информацию о созданной заявке")
    def close_created_dialog(self) -> Self:
        self.created_dialog_close_button.click()

        return self
