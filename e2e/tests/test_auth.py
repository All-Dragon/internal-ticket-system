import allure
import pytest
from playwright.sync_api import expect

from e2e.fixtures.auth import AdminCredentials
from e2e.pages.ticket_page import TicketPage


@allure.feature("Авторизация")
@allure.story("Вход Администратора")
@allure.title("Администратор успешно входит с корректными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_admin_can_login(
    ticket_page: TicketPage,
    admin_credentials: AdminCredentials,
):
    ticket_page.open()
    ticket_page.login(
        username=admin_credentials.username,
        password=admin_credentials.password
    )
    
    with allure.step("Проверить успешную авторизацию"):
        expect(ticket_page.admin_status).to_be_visible()
        expect(ticket_page.logout_button).to_be_enabled()
        expect(ticket_page.login_button).not_to_be_visible()
    

@allure.feature("Авторизация")
@allure.story("Вход Администратора")
@allure.title("Вход невозможен с незаполненными обязательными полями")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password", 
    [
        ("", ""),
        ("test@mail.ru", ""),
        ("", "testpassword"),
    ], 
    ids = ["Пустые значения", "Почта без пароля", "Пароль без почты"])
def test_admin_cannot_login_with_missing_credentials(
    ticket_page: TicketPage,
    username: str,
    password: str 
):
    ticket_page.open()
    ticket_page.login(
        username=username,
        password=password
    )
    
    with allure.step("Проверить сообщение об обязательных полях"):
        expect(ticket_page.error_message).to_contain_text("Введите логин и пароль администратора")
        expect(ticket_page.admin_status).not_to_be_visible()
        expect(ticket_page.logout_button).not_to_be_visible()
        
    
@allure.feature("Авторизация")
@allure.story("Вход Администратора")
@allure.title("Вход невозможен с неверными учётными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password",
    [
        ("test@mail.ru", "wrong-password"),
        ("unknown@mail.ru", "testpassword"),
    ],
    ids=[
        "Неверный пароль",
        "Неизвестный пользователь",
    ],
)
def test_admin_cannot_login_with_invalid_credentials(
    ticket_page: TicketPage,
    username: str,
    password: str,
):
    ticket_page.open()
    ticket_page.login(
        username=username,
        password=password,
    )

    with allure.step("Проверить ошибку неверных учётных данных"):
        expect(ticket_page.error_message).to_contain_text(
            "Неверный логин или пароль администратора"
        )
        expect(ticket_page.admin_status).not_to_be_visible()
        expect(ticket_page.logout_button).not_to_be_visible()
        
        
        
@allure.feature("Авторизация")
@allure.story("Обработка ошибок авторизации")
@allure.title("Администратор может закрыть сообщение об ошибке авторизации")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_admin_can_close_login_error(
    ticket_page: TicketPage,
):
    ticket_page.open()

    ticket_page.login(
        username="wrong@mail.ru",
        password="wrong-password",
    )

    with allure.step("Проверить отображение ошибки авторизации"):
        expect(ticket_page.error_message).to_be_visible()

    ticket_page.close_login_error()

    with allure.step("Проверить закрытие сообщения об ошибке"):
        expect(ticket_page.error_message).not_to_be_visible()


@allure.feature("Авторизация")
@allure.story("Выход Администратора")
@allure.title("Администратор успешно выходит из аккаунта")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
def test_admin_can_logout(
    admin_ticket_page: TicketPage
):
    admin_ticket_page.logout()

    with allure.step("Проверить успешный выход администратора"):
        expect(admin_ticket_page.admin_status).not_to_be_visible()
        expect(admin_ticket_page.logout_button).not_to_be_visible()
        expect(admin_ticket_page.login_button).to_be_visible()
        expect(admin_ticket_page.login_button).to_be_enabled()
    