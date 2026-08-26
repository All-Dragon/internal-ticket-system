from dataclasses import dataclass
from uuid import uuid4

import allure
import pytest
from playwright.sync_api import Page, expect

from e2e.models.ticket import TicketPriority, TicketStatus
from e2e.pages.ticket_page import TicketPage


@dataclass(frozen=True, slots=True)
class TicketData:
    title: str
    description: str
    priority: TicketPriority


@pytest.fixture
def ticket_data_factory():
    def build_ticket(
        title: str | None = None,
        description: str | None = None,
        priority: TicketPriority = TicketPriority.NORMAL,
    ) -> TicketData:
        unique_id = uuid4().hex[:8]

        return TicketData(
            title=title or f"E2E заявка {unique_id}",
            description=description or f"Описание E2E заявки {unique_id}",
            priority=priority,
        )

    return build_ticket


@dataclass(frozen=True, slots=True)
class CreatedTicket:
    id: int
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus


@pytest.fixture
def ticket_creator(
    page: Page,
    ticket_data_factory,
):
    @allure.step("Подготовить заявку через API")
    def create_ticket(
        title: str | None = None,
        description: str | None = None,
        priority: TicketPriority = TicketPriority.NORMAL,
    ) -> CreatedTicket:
        ticket = ticket_data_factory(
            title=title,
            description=description,
            priority=priority,
        )

        response = page.request.post(
            "/tickets",
            data={
                "title": ticket.title,
                "description": ticket.description,
                "priority": ticket.priority.value,
            },
        )

        assert response.status == 201

        response_data = response.json()

        return CreatedTicket(
            id=response_data["id"],
            title=response_data["title"],
            description=response_data["description"],
            priority=TicketPriority(response_data["priority"]),
            status=TicketStatus(response_data["status"]),
        )

    return create_ticket


@pytest.fixture
def ticket_editor(
    ticket_page: TicketPage,
    ticket_creator,
    ticket_data_factory,
):
    @allure.step("Подготовить отредактированную заявку")
    def edit_ticket(
        ticket: CreatedTicket | None = None,
        title: str | None = None,
        description: str | None = None,
        priority: TicketPriority = TicketPriority.HIGH,
    ) -> CreatedTicket:
        current_ticket = ticket or ticket_creator()

        updated_ticket = ticket_data_factory(
            title=title,
            description=description,
            priority=priority,
        )

        ticket_page.open()
        ticket_page.ticket_table.edit_button(
            current_ticket.id
        ).click()

        with ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "PATCH"
                and response.url.endswith(
                    f"/tickets/{current_ticket.id}"
                )
            )
        ) as response_info:
            ticket_page.edit_modal.edit(
                ticket_id=current_ticket.id,
                title=updated_ticket.title,
                description=updated_ticket.description,
                priority=priority,
            )

        response = response_info.value
        assert response.status == 200

        response_data = response.json()

        expect(
            ticket_page.edit_modal.dialog(current_ticket.id)
        ).not_to_be_visible()

        return CreatedTicket(
            id=response_data["id"],
            title=response_data["title"],
            description=response_data["description"],
            priority=TicketPriority(response_data["priority"]),
            status=TicketStatus(response_data["status"]),
        )

    return edit_ticket
