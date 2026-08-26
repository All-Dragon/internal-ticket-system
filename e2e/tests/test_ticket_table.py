import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage
from e2e.models.ticket import TicketStatus

@allure.feature("Заявки")
@allure.story("Таблица заявок")
@allure.title("Созданная заявка появляется в таблице")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_created_ticket_is_displayed_in_table(
    ticket_page: TicketPage,
    ticket_data_factory,
):
    ticket = ticket_data_factory(priority="high")
    ticket_page.open()
    
    with ticket_page.page.expect_response(
        lambda response: (
            response.request.method == "POST"
            and response.url.endswith("/tickets")
        )
    ) as response:
        ticket_page.create_form.create(
            title=ticket.title,
            description=ticket.description,
            priority=ticket.priority,
        )
        
    response = response.value
    
    with allure.step("Получить ID созданной заявки"):
        assert response.status == 201
        ticket_id = response.json()["id"]
        
    ticket_page.create_form.close_created_dialog()
    
    row = ticket_page.ticket_table.row_by_id(ticket_id)
    
    with allure.step("Проверить созданную заявку в таблице"):
        expect(row).to_be_visible()

        expect(
            ticket_page.ticket_table.title_in_row(ticket_id)
        ).to_have_text(ticket.title)

        expect(
            ticket_page.ticket_table.description_in_row(ticket_id)
        ).to_have_text(ticket.description)

        expect(
            ticket_page.ticket_table.priority_in_row(ticket_id)
        ).to_have_text("High")

        expect(
            ticket_page.ticket_table.status_in_row(ticket_id)
        ).to_have_value("new")
        
@allure.feature("Заявки")
@allure.story("Таблица заявок")
@allure.title("Статус заявки изменяется и сохраняется")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_ticket_status_can_be_changed(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator()
    ticket_page.open()

    with allure.step("Проверить начальный статус заявки"):
        expect(
            ticket_page.ticket_table.status_in_row(ticket.id)
        ).to_have_value(TicketStatus.NEW.value)

    with allure.step("Изменить статус заявки"):
        with ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "PATCH"
                and response.url.endswith(
                    f"/tickets/{ticket.id}/status"
                )
            )
        ) as response_info:
            ticket_page.ticket_table.change_status(
                ticket.id,
                TicketStatus.IN_PROGRESS,
            )

        response = response_info.value
        response_data = response.json()

        assert response.status == 200
        assert (
            response_data["status"]
            == TicketStatus.IN_PROGRESS.value
        )

    with allure.step("Проверить новый статус в таблице"):
        expect(
            ticket_page.ticket_table.status_in_row(ticket.id)
        ).to_have_value(TicketStatus.IN_PROGRESS.value)

    ticket_page.page.reload()

    with allure.step("Проверить статус после перезагрузки"):
        expect(
            ticket_page.ticket_table.row_by_id(ticket.id)
        ).to_be_visible()

        expect(
            ticket_page.ticket_table.status_in_row(ticket.id)
        ).to_have_value(TicketStatus.IN_PROGRESS.value)