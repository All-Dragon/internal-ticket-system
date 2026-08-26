import allure
import pytest
from playwright.sync_api import expect

from e2e.models.ticket import TicketPriority, TicketStatus
from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Просмотр заявки")
@allure.title("Пользователь просматривает данные заявки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_user_can_view_ticket_details(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        priority=TicketPriority.HIGH,
    )
    
    ticket_page.open()
    
    with allure.step("Открыть подробности заявки"):
        ticket_page.ticket_table.view_button(
            ticket.id
        ).click()
        
    with allure.step("Проверить открытие окна"):
        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Проверить данные заявки"):
        expect(
            ticket_page.details_modal.title(ticket.id)
            ).to_have_text(ticket.title)
        
        expect(
            ticket_page.details_modal.description(ticket.id)
        ).to_have_text(ticket.description)
        
        expect(
            ticket_page.details_modal.status(ticket.id)
        ).to_have_text("New")

        expect(
            ticket_page.details_modal.priority(ticket.id)
        ).to_have_text("High")

        expect(
            ticket_page.details_modal.created_at(ticket.id)
        ).to_be_visible()

        expect(
            ticket_page.details_modal.updated_at(ticket.id)
        ).to_be_visible()
        
@allure.feature("Заявки")
@allure.story("Просмотр заявки")
@allure.title(
    "После редактирования из окна просмотра отображаются новые данные"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_details_display_data_updated_from_details_dialog(
    ticket_page: TicketPage,
    ticket_creator,
    ticket_data_factory,
):
    ticket = ticket_creator()
    updated_ticket = ticket_data_factory(
        priority=TicketPriority.HIGH,
    )
    
    ticket_page.open()
    
    with allure.step("Открыть подробности заявки"):
        ticket_page.ticket_table.view_button(
            ticket.id
        ).click()

        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Перейти к редактированию"):
        ticket_page.details_modal.edit_button(
            ticket.id
        ).click()

        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).not_to_be_visible()

        expect(
            ticket_page.edit_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Изменить данные заявки"):
        with ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "PATCH"
                and response.url.endswith(
                    f"/tickets/{ticket.id}"
                )
            )
        ) as response:
            ticket_page.edit_modal.edit(
                ticket_id=ticket.id,
                title=updated_ticket.title,
                description=updated_ticket.description,
                priority=TicketPriority.HIGH,
            )

        assert response.value.status == 200

        expect(
            ticket_page.edit_modal.dialog(ticket.id)
        ).not_to_be_visible()
        
    with allure.step("Повторно открыть подробности заявки"):
        ticket_page.ticket_table.view_button(
            ticket.id
        ).click()

        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Проверить обновлённые данные"):
        expect(
            ticket_page.details_modal.title(ticket.id)
        ).to_have_text(updated_ticket.title)

        expect(
            ticket_page.details_modal.description(ticket.id)
        ).to_have_text(updated_ticket.description)

        expect(
            ticket_page.details_modal.priority(ticket.id)
        ).to_have_text("High")

        expect(
            ticket_page.details_modal.status(ticket.id)
        ).to_have_text("New")
        
        
@allure.feature("Заявки")
@allure.story("Просмотр заявки")
@allure.title(
    "Завершённую заявку нельзя редактировать из окна просмотра"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_done_ticket_cannot_be_edited_from_details(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        status=TicketStatus.DONE,
    )

    ticket_page.open()
    ticket_page.ticket_table.view_button(ticket.id).click()

    with allure.step("Проверить завершённый статус"):
        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()

        expect(
            ticket_page.details_modal.status(ticket.id)
        ).to_have_text("Done")

    with allure.step("Проверить запрет редактирования"):
        edit_button = (
            ticket_page.details_modal.edit_button(ticket.id)
        )

        expect(edit_button).to_be_disabled()
        expect(edit_button).to_have_attribute(
            "title",
            "Заявку в статусе Done нельзя редактировать",
        )

        expect(
            ticket_page.details_modal.completed_ticket_hint(
                ticket.id
            )
        ).to_be_visible()