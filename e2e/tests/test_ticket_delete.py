import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage
from e2e.models.ticket import TicketStatus 

@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title("Администратор удаляет заявку из таблицы")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_admin_can_delete_ticket_from_table(
    admin_ticket_page: TicketPage,
    ticket_creator,
):
    ticket=ticket_creator()
    
    admin_ticket_page.open()
    
    with allure.step("Открыть подтверждение удаления"):
        admin_ticket_page.ticket_table.delete_button(
            ticket.id
        ).click()

        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).to_be_visible()

        expect(
            admin_ticket_page.delete_modal.ticket_info(
                ticket.id
            )
        ).to_have_text(
            f"#{ticket.id} {ticket.title}"
        )

        expect(
            admin_ticket_page.delete_modal.warning(
                ticket.id
            )
        ).to_be_visible()
        
    with allure.step("Подтвердить удаление"):
         with admin_ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "DELETE"
                and response.url.endswith(
                    f"/tickets/{ticket.id}"
                )
            )
        ) as response:
            admin_ticket_page.delete_modal.confirm(
                ticket.id
            )

    assert response.value.status == 204
    
    with allure.step("Проверить удаление заявки"):
        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).not_to_be_visible()

        expect(
            admin_ticket_page.ticket_table.row_by_id(ticket.id)
        ).not_to_be_visible()
        
@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title("Администратор удаляет заявку из окна просмотра")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_admin_can_delete_ticket_from_details(
    admin_ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator()

    admin_ticket_page.open()

    with allure.step("Открыть подробности заявки"):
        admin_ticket_page.ticket_table.view_button(
            ticket.id
        ).click()

        expect(
            admin_ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()

    with allure.step("Перейти к удалению"):
        admin_ticket_page.details_modal.delete_button(
            ticket.id
        ).click()

        expect(
            admin_ticket_page.details_modal.dialog(ticket.id)
        ).not_to_be_visible()

        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).to_be_visible()

        expect(
            admin_ticket_page.delete_modal.ticket_info(
                ticket.id
            )
        ).to_have_text(
            f"#{ticket.id} {ticket.title}"
        )

    with allure.step("Подтвердить удаление"):
        with admin_ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "DELETE"
                and response.url.endswith(
                    f"/tickets/{ticket.id}"
                )
            )
        ) as response_info:
            admin_ticket_page.delete_modal.confirm(
                ticket.id
            )

        assert response_info.value.status == 204

    with allure.step("Проверить результат удаления"):
        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).not_to_be_visible()

        expect(
            admin_ticket_page.ticket_table.row_by_id(ticket.id)
        ).not_to_be_visible()
        
        
@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title(
    "Завершённую заявку нельзя удалить из таблицы"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_done_ticket_cannot_be_deleted_from_table(
    admin_ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        status=TicketStatus.DONE,
    )

    admin_ticket_page.open()

    with allure.step("Проверить завершённый статус"):
        expect(
            admin_ticket_page.ticket_table.status_in_row(
                ticket.id
            )
        ).to_have_value(TicketStatus.DONE.value)

    with allure.step("Проверить запрет удаления"):
        delete_button = (
            admin_ticket_page.ticket_table.delete_button(
                ticket.id
            )
        )

        expect(delete_button).to_be_disabled()
        expect(delete_button).to_have_attribute(
            "title",
            "Заявку в статусе Done нельзя удалить",
        )

        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).not_to_be_visible()
        
@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title(
    "Завершённую заявку нельзя удалить из окна просмотра"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_done_ticket_cannot_be_deleted_from_details(
    admin_ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        status=TicketStatus.DONE,
    )

    admin_ticket_page.open()
    admin_ticket_page.ticket_table.view_button(
        ticket.id
    ).click()

    with allure.step("Проверить завершённый статус"):
        expect(
            admin_ticket_page.details_modal.status(ticket.id)
        ).to_have_text("Done")

    with allure.step("Проверить запрет удаления"):
        delete_button = (
            admin_ticket_page.details_modal.delete_button(
                ticket.id
            )
        )

        expect(delete_button).to_be_disabled()
        expect(delete_button).to_have_attribute(
            "title",
            "Заявку в статусе Done нельзя удалить",
        )

        expect(
            admin_ticket_page.details_modal.completed_ticket_hint(
                ticket.id
            )
        ).to_be_visible()

        expect(
            admin_ticket_page.delete_modal.dialog(ticket.id)
        ).not_to_be_visible()
        
        
@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title(
    "Неавторизованный пользователь не может удалить заявку из таблицы"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_user_cannot_delete_ticket_from_table(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator()

    ticket_page.open()

    with allure.step("Проверить отсутствие прав администратора"):
        expect(
            ticket_page.auth.login_button
        ).to_be_visible()

    with allure.step("Проверить отсутствие кнопки удаления"):
        expect(
            ticket_page.ticket_table.delete_button(ticket.id)
        ).to_have_count(0)
        

@allure.feature("Заявки")
@allure.story("Удаление заявки")
@allure.title(
    "Неавторизованный пользователь не может удалить заявку из окна просмотра"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_user_cannot_delete_ticket_from_details(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator()
    
    ticket_page.open()
    ticket_page.ticket_table.view_button(ticket.id).click()
    
    with allure.step("Проверить открытие окна просмотра"):
        expect(
            ticket_page.details_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Проверить отсутствие кнопки удаления"):
        expect(
            ticket_page.details_modal.delete_button(ticket.id)
        ).to_have_count(0)
