import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage
from e2e.fixtures.tickets import TicketData

@pytest.fixture
def created_ticket(
    ticket_page: TicketPage,
    ticket_data_factory,
) -> TicketData:
    ticket = ticket_data_factory(priority="high")

    ticket_page.open()
    ticket_page.create_form.create(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
    )

    expect(
        ticket_page.create_form.created_dialog
    ).to_be_visible()

    return ticket


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
            "x" * 121,
            "Корректное описание",
            "title",
            "Название должно быть не длиннее 120 символов",
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
        "Длинный заголовок",
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


@allure.feature("Заявки")
@allure.story("Создание заявки")
@allure.title("Данные созданной заявки отображаются в модальном окне")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_created_ticket_data_is_shown_in_dialog(
    ticket_page: TicketPage,
    created_ticket: TicketData,
):
    dialog = ticket_page.create_form.created_dialog

    with allure.step("Проверить данные созданной заявки"):
        expect(dialog).to_contain_text(created_ticket.title)
        expect(dialog).to_contain_text(
            created_ticket.description
        )
        expect(dialog).to_contain_text("High")
        expect(dialog).to_contain_text("New")


@allure.feature("Заявки")
@allure.story("Создание заявки")
@allure.title("Пользователь закрывает окно созданной заявки")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.usefixtures("created_ticket")
def test_user_can_close_created_ticket_dialog(
    ticket_page: TicketPage,
):
    ticket_page.create_form.close_created_dialog()

    with allure.step("Проверить закрытие модального окна"):
        expect(
            ticket_page.create_form.created_dialog
        ).not_to_be_visible()


@allure.feature("Заявки")
@allure.story("Создание заявки")
@allure.title("Форма очищается после успешного создания заявки")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.usefixtures("created_ticket")
def test_create_ticket_form_is_reset_after_success(
    ticket_page: TicketPage,
):
    form = ticket_page.create_form

    with allure.step("Проверить очищенные поля формы"):
        expect(form.title_input).to_have_value("")
        expect(form.description_input).to_have_value("")
        expect(form.priority_select).to_have_value("normal")


@allure.feature("Заявки")
@allure.story("Граничные значения формы создания заявки")
@allure.title("Заявка создаётся с допустимой длиной заголовка")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "title_length",
    [
        3,
        120,
    ],
    ids=[
        "Минимальная длина заголовка",
        "Максимальная длина заголовка",
    ],
)
def test_ticket_can_be_created_with_boundary_title_length(
    ticket_page: TicketPage,
    ticket_data_factory,
    title_length: int,
):
    ticket = ticket_data_factory(
        title="T" * title_length,
    )

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

    with allure.step("Проверить создание заявки"):
        assert response.value.status == 201
        expect(
            ticket_page.create_form.created_dialog
        ).to_be_visible()
        expect(
            ticket_page.create_form.created_dialog
        ).to_contain_text(ticket.title)


@allure.feature("Заявки")
@allure.story("Граничные значения формы создания заявки")
@allure.title("Заявка создаётся с описанием максимальной длины")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_ticket_can_be_created_with_max_description_length(
    ticket_page: TicketPage,
    ticket_data_factory,
):
    ticket = ticket_data_factory(
        description="D" * 1000,
    )

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

    with allure.step("Проверить создание заявки"):
        assert response.value.status == 201
        expect(
            ticket_page.create_form.created_dialog
        ).to_be_visible()

    with allure.step("Проверить описание созданной заявки"):
        expect(
            ticket_page.create_form.created_dialog
        ).to_contain_text(ticket.description)
