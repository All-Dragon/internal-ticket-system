import allure
from playwright.sync_api import Locator, Page


class TicketDetailsModal:
    def __init__(self, page: Page):
        self.page = page

    def dialog(self, ticket_id: int) -> Locator:
        return self.page.get_by_role(
            "dialog",
            name="Подробности заявки",
            exact=True,
        ).filter(
            has=self.page.get_by_text(
                f"#{ticket_id}",
                exact=True,
            )
        )

    def ticket_id(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_text(
            f"#{ticket_id}",
            exact=True,
        )

    def title(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).locator("header strong")

    def description(self, ticket_id: int) -> Locator:
        section = self.dialog(ticket_id).get_by_role(
            "region",
            name="Описание",
            exact=True,
        )
        return section.get_by_role("paragraph")

    def status(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_test_id("ticket-status")

    def priority(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_test_id("ticket-priority")

    def created_at(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_test_id("ticket-created-at")

    def updated_at(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_test_id("ticket-updated-at")

    def close_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Закрыть подробности заявки",
            exact=True,
        )

    def edit_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Редактировать",
            exact=True,
        )

    def delete_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Удалить заявку",
            exact=True,
        )

    def completed_ticket_hint(
        self,
        ticket_id: int,
    ) -> Locator:
        return self.dialog(ticket_id).get_by_text(
            (
                "Завершённые заявки недоступны "
                "для редактирования и удаления."
            ),
            exact=True,
        )

    @allure.step("Закрыть подробности заявки #{ticket_id}")
    def close(self, ticket_id: int) -> None:
        self.close_button(ticket_id).click()