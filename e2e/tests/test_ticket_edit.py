import allure
import pytest
from playwright.sync_api import expect

from e2e.models.ticket import TicketPriority, TicketStatus
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


@allure.feature("Заявки")
@allure.story("Валидация формы редактирования заявки")
@allure.title("Форма реактивно валидирует изменяемое поле")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    (
        "invalid_field",
        "invalid_value",
        "expected_error",
    ),
    [
        (
            "title",
            "ab",
            "Название должно быть не короче 3 символов",
        ),
        (
            "title",
            "x" * 121,
            "Название должно быть не длиннее 120 символов",
        ),
        (
            "title",
            "",
            "Название заявки обязательно",
        ),
        (
            "description",
            "x" * 1001,
            "Описание должно быть не длиннее 1000 символов",
        ),
    ],
    ids=[
        "short-title",
        "long-title",
        "empty-title",
        "long-description",
    ],
)
def test_edit_form_reactively_validates_field(
    ticket_page: TicketPage,
    ticket_creator,
    invalid_field: str,
    invalid_value: str,
    expected_error: str,
):
    ticket = ticket_creator()

    ticket_page.open()
    ticket_page.ticket_table.edit_button(ticket.id).click()

    field = getattr(
        ticket_page.edit_modal,
        f"{invalid_field}_input"
    )(ticket.id)

    error = getattr(
        ticket_page.edit_modal,
        f"{invalid_field}_error"
    )(ticket.id)

    with allure.step("Ввести невалидное значение"):
        field.fill(invalid_value)

    with allure.step("Проверить появление ошибки"):
        expect(error).to_be_visible()
        expect(error).to_have_text(expected_error)
        expect(field).to_have_attribute(
            "aria-invalid",
            "true",
        )

    valid_value = (
        ticket.title
        if invalid_field == "title"
        else ticket.description
    )

    with allure.step("Исправить значение поля"):
        field.fill(valid_value)

    with allure.step("Проверить исчезновение ошибки"):
        expect(error).not_to_be_visible()
        expect(field).to_have_attribute(
            "aria-invalid",
            "false",
        )


@allure.feature("Заявки")
@allure.story("Валидация формы редактирования заявки")
@allure.title("Форма не сохраняет невалидные изменения")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_invalid_edit_is_not_saved(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator()

    ticket_page.open()
    ticket_page.ticket_table.edit_button(ticket.id).click()

    title_input = ticket_page.edit_modal.title_input(
        ticket.id
    )
    title_error = ticket_page.edit_modal.title_error(
        ticket.id
    )

    with allure.step("Очистить обязательное поле"):
        title_input.fill("")

    with allure.step("Попытаться сохранить форму"):
        ticket_page.edit_modal.save_button(
            ticket.id
        ).click()

    with allure.step("Проверить отклонение изменений"):
        expect(title_error).to_be_visible()
        expect(title_error).to_have_text(
            "Название заявки обязательно"
        )
        expect(title_input).to_have_attribute(
            "aria-invalid",
            "true",
        )
        expect(
            ticket_page.edit_modal.dialog(ticket.id)
        ).to_be_visible()

    ticket_page.edit_modal.cancel_button(
        ticket.id
    ).click()

    with allure.step("Проверить исходные данные в таблице"):
        expect(
            ticket_page.edit_modal.dialog(ticket.id)
        ).not_to_be_visible()

        expect(
            ticket_page.ticket_table.title_in_row(ticket.id)
        ).to_have_text(ticket.title)


@allure.feature("Заявки")
@allure.story("Редактирование заявки")
@allure.title(
    "Завершённую заявку нельзя редактировать из таблицы"
)
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_done_ticket_cannot_be_edited_from_table(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        status=TicketStatus.DONE,
    )

    ticket_page.open()

    with allure.step("Проверить статус заявки"):
        expect(
            ticket_page.ticket_table.status_in_row(ticket.id)
        ).to_have_value(TicketStatus.DONE.value)

    with allure.step("Проверить запрет редактирования"):
        edit_button = (
            ticket_page.ticket_table.edit_button(ticket.id)
        )

        expect(edit_button).to_be_disabled()
        expect(edit_button).to_have_attribute(
            "title",
            "Заявку в статусе Done нельзя редактировать",
        )
