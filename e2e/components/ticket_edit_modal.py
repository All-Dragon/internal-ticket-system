import allure
from playwright.sync_api import Locator, Page

from e2e.models.ticket import TicketPriority


class TicketEditModal:
    def __init__(self, page: Page):
        self.page = page

    def dialog(self, ticket_id: int) -> Locator:
        return self.page.get_by_role(
            "dialog",
            name=f"Редактировать заявку #{ticket_id}",
            exact=True,
        )

    def title_input(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "textbox",
            name="Заголовок",
            exact=True,
        )

    def description_input(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "textbox",
            name="Описание",
            exact=True,
        )

    def priority_select(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "combobox",
            name="Приоритет",
            exact=True,
        )

    def save_button(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).get_by_role(
            "button",
            name="Сохранить",
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
            name="Закрыть окно редактирования",
            exact=True,
        )

    def title_error(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).locator(
            "#edit-ticket-title-error"
        )

    def description_error(self, ticket_id: int) -> Locator:
        return self.dialog(ticket_id).locator(
            "#edit-ticket-description-error"
        )

    @allure.step("Изменить данные заявки #{ticket_id}")
    def edit(
        self,
        ticket_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: TicketPriority | None = None,
    ) -> None:
        if title is not None:
            self.title_input(ticket_id).fill(title)

        if description is not None:
            self.description_input(ticket_id).fill(description)

        if priority is not None:
            self.priority_select(ticket_id).select_option(priority.value)

        self.save_button(ticket_id).click()
