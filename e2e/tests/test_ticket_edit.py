import allure
import pytest
from playwright.sync_api import expect

from e2e.models.ticket import TicketPriority
from e2e.pages.ticket_page import TicketPage

@allure.feature("Заявки")
@allure.story("Редактирование заявки")
@allure.title("Пользователь успешно редактирует заявку")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_ticket_can_be_edited(
    ticket_page: TicketPage,
    ticket_creator,
    ticket_data_factory,
):
    ticket = ticket_creator()
    updated_ticket = ticket_data_factory(priority="high")
    
    ticket_page.open()
    ticket_page.ticket_table.edit_button(ticket.id).click()
    
    with allure.step("Проверить открытие окна редактирования"):
        expect(
            ticket_page.edit_modal.dialog(ticket.id)
        ).to_be_visible()
        
    with allure.step("Изменить данные заявки"):
        with ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "PATCH"
                and response.url.endswith(f"/tickets/{ticket.id}")
            )
        ) as response:
            ticket_page.edit_modal.edit(
                ticket_id=ticket.id,
                title=updated_ticket.title,
                description=updated_ticket.description,
                priority=TicketPriority.HIGH,
            )
            
        response = response.value 
        response_data = response.json()
        
        assert response.status == 200
        
        assert response_data["title"] == updated_ticket.title
        assert (
            response_data["description"]
            == updated_ticket.description
        )
        assert response_data["priority"] == TicketPriority.HIGH.value

        with allure.step("Проверить закрытие окна"):
            expect(
                ticket_page.edit_modal.dialog(ticket.id)
            ).not_to_be_visible()
            
        with allure.step("Проверить изменённые данные в таблице"):
            expect(
                ticket_page.ticket_table.title_in_row(ticket.id)
                ).to_have_text(updated_ticket.title)
            
            expect(
                ticket_page.ticket_table.description_in_row(ticket.id)
            ).to_have_text(updated_ticket.description)

            expect(
                ticket_page.ticket_table.priority_in_row(ticket.id)
            ).to_have_text("High")
            
            
@pytest.mark.parametrize(
    (
        "new_title",
        "new_description",
        "new_priority",
    ),
    [
        (
            "Изменённый заголовок",
            None,
            None,
        ),
        (
            None,
            "Изменённое описание заявки",
            None,
        ),
        (
            None,
            None,
            TicketPriority.HIGH,
        ),
    ],
    ids=[
        "only-title",
        "only-description",
        "only-priority",
    ],
)
@allure.feature("Заявки")
@allure.story("Редактирование заявки")
@allure.title("При изменении одного поля остальные поля сохраняются")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
def test_editing_one_field_preserves_other_fields(
    ticket_page: TicketPage,
    ticket_creator,
    new_title: str | None,
    new_description: str | None,
    new_priority: TicketPriority | None,
):
    ticket = ticket_creator()

    expected_title = (
        new_title
        if new_title is not None
        else ticket.title
    )
    expected_description = (
        new_description
        if new_description is not None
        else ticket.description
    )
    expected_priority = (
        new_priority.value
        if new_priority is not None
        else ticket.priority
    )

    ticket_page.open()
    ticket_page.ticket_table.edit_button(ticket.id).click()

    with ticket_page.page.expect_response(
        lambda response: (
            response.request.method == "PATCH"
            and response.url.endswith(f"/tickets/{ticket.id}")
        )
    ) as response_info:
        ticket_page.edit_modal.edit(
            ticket_id=ticket.id,
            title=new_title,
            description=new_description,
            priority=new_priority,
        )

    response = response_info.value
    response_data = response.json()

    with allure.step("Проверить сохранённые данные заявки"):
        assert response.status == 200
        assert response_data["title"] == expected_title
        assert (
            response_data["description"]
            == expected_description
        )
        assert response_data["priority"] == expected_priority
        assert response_data["status"] == ticket.status.value

    with allure.step("Проверить данные заявки в таблице"):
        expect(
            ticket_page.ticket_table.title_in_row(ticket.id)
        ).to_have_text(expected_title)

        expect(
            ticket_page.ticket_table.description_in_row(ticket.id)
        ).to_have_text(expected_description)

        expect(
            ticket_page.ticket_table.priority_in_row(ticket.id)
        ).to_have_text(expected_priority.capitalize())
        
        
@allure.feature("Заявки")
@allure.story("Редактирование заявки")
@allure.title("Изменения заявки сохраняются после перезагрузки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_edited_ticket_is_persisted_after_reload(
    ticket_page: TicketPage,
    ticket_editor,
):
    ticket = ticket_editor()
    
    with allure.step("Перезагрузить страницу"):
        with ticket_page.page.expect_response(
            lambda response: (
                response.request.method == "GET"
                and response.url.partition("?")[0].endswith(
                    "/tickets"
                )
            )
        ) as response_info:
            ticket_page.page.reload()
    
    assert response_info.value.status == 200
    
    with allure.step("Проверить загруженные данные заявки"):
        expect(
            ticket_page.ticket_table.row_by_id(ticket.id)
        ).to_be_visible()

        expect(
            ticket_page.ticket_table.title_in_row(ticket.id)
        ).to_have_text(ticket.title)

        expect(
            ticket_page.ticket_table.description_in_row(ticket.id)
        ).to_have_text(ticket.description)

        expect(
            ticket_page.ticket_table.priority_in_row(ticket.id)
        ).to_have_text(ticket.priority.value.capitalize())