import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Создание заявки")
@allure.title("Пользователь успешно создаёт заявку")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_user_can_create_ticket(
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

    with allure.step("Проверить успешное создание заявки"):
        assert response.value.status == 201
        expect(ticket_page.create_form.created_dialog).to_be_visible()


@allure.feature("Заявки")
@allure.story("Валидация формы создания заявки")
@allure.title("Форма не принимает невалидные данные")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    (
        "title",
        "description",
        "invalid_field",
        "expected_error",
    ),
    [
        (
            "ab",
            "Корректное описание",
            "title",
            "Название должно быть не короче 3 символов",
        ),
        (
            "Корректный заголовок",
            "x" * 1001,
            "description",
            "Описание должно быть не длиннее 1000 символов",
        ),
        (
            "",
            "",
            "title",
            "Название заявки обязательно",
        ),
    ],
    ids=[
        "Короткий заголовок",
        "Длинное описание",
        "Пустая форма",
    ],
)
def test_ticket_is_not_created_with_invalid_data(
    ticket_page: TicketPage,
    title: str,
    description: str,
    invalid_field: str,
    expected_error: str,
):
    ticket_page.open()

    ticket_page.create_form.create(
        title=title,
        description=description,
        priority="normal",
    )

    field = getattr(
        ticket_page.create_form,
        f"{invalid_field}_input",
    )
    error = getattr(
        ticket_page.create_form,
        f"{invalid_field}_error",
    )

    with allure.step("Проверить ошибку клиентской валидации"):
        expect(error).to_be_visible()
        expect(error).to_have_text(expected_error)
        expect(field).to_have_attribute(
            "aria-invalid",
            "true",
        )

    with allure.step("Проверить, что заявка не создана"):
        expect(
            ticket_page.create_form.created_dialog
        ).not_to_be_visible()
