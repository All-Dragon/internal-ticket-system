from playwright.sync_api import Locator, Page

from e2e.models import TicketStatus


class TicketQuickFilters:
    def __init__(self, page: Page):
        self.root = page.get_by_role(
            "group",
            name="Быстрые фильтры",
            exact=True,
        )

        self.all_tickets_button = self.root.get_by_role(
            "button",
            name="Все заявки",
            exact=True,
        )

        self.new_button = self.root.get_by_role(
            "button",
            name="Новые",
            exact=True,
        )

        self.in_progress_button = self.root.get_by_role(
            "button",
            name="В работе",
            exact=True,
        )

        self.done_button = self.root.get_by_role(
            "button",
            name="Закрытые",
            exact=True,
        )

        self.high_priority_button = self.root.get_by_role(
            "button",
            name="Высокий приоритет",
            exact=True,
        )

    def status_button(
        self,
        status: TicketStatus,
    ) -> Locator:
        buttons = {
            TicketStatus.NEW: self.new_button,
            TicketStatus.IN_PROGRESS: self.in_progress_button,
            TicketStatus.DONE: self.done_button,
        }

        return buttons[status]

    def filter_by_status(
        self,
        status: TicketStatus,
    ) -> None:
        self.status_button(status).click()

    def filter_by_high_priority(self) -> None:
        self.high_priority_button.click()

    def show_all_tickets(self) -> None:
        self.all_tickets_button.click()
