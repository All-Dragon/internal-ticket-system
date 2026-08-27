import re

import allure
from playwright.sync_api import Locator, Page


class TicketDeleteConfirmModal:
    def __init__(self, page: Page):
        self.page = page

    def dialog(self, ticket_id: int) -> Locator:
        return self.page.get_by_role(
            "alertdialog",
            name="Удалить заявку?",
            exact=True,
        ).filter(
            has=self.page.get_by_text(
                re.compile(rf"^#{ticket_id}\s"),
            )
        )

    def ticket_info(self, ticket_id: int) -> Locator:
        return (
            self.dialog(ticket_id)
            .locator("header")
            .get_by_role("paragraph")
        )

    def warning(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_text(
            (
                "Это действие нельзя отменить. "
                "Заявка будет удалена из системы."
            ),
            exact=True,
        )

    def cancel_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Отмена",
            exact=True,
        )

    def close_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Закрыть подтверждение удаления",
            exact=True,
        )

    def confirm_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Удалить заявку",
            exact=True,
        )

    @allure.step("Подтвердить удаление заявки #{ticket_id}")
    def confirm(self, ticket_id: int) -> None:
        self.confirm_button(ticket_id).click()

    @allure.step("Отменить удаление заявки #{ticket_id}")
    def cancel(self, ticket_id: int) -> None:
        self.cancel_button(ticket_id).click()

    @allure.step("Закрыть окно подтверждения удаления заявки #{ticket_id}")
    def close(self, ticket_id: int) -> None:
        self.close_button(ticket_id).click()
