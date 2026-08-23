from typing import Self

import allure
from playwright.sync_api import Page 

class TicketPage:
    
    URL = '/'
    
    def __init__(self, page: Page):
        self.page = page 
        
        self.page_heading = page.get_by_role(
            "heading",
            name="Внутренние заявки",
            exact=True,
        )

        self.username_input = page.get_by_placeholder(
            "Логин",
            exact=True,
        )
        self.password_input = page.get_by_placeholder(
            "Пароль",
            exact=True,
        )
        self.login_button = page.get_by_role(
            "button",
            name="Войти",
            exact=True,
        )
        self.logout_button = page.get_by_role(
            "button",
            name="Выйти"
        )
        self.admin_status = page.get_by_text(
            "Вы вошли как администратор",
            exact=True
        )
        
        self.error_message = page.get_by_role("alert").filter(
            has=page.get_by_role(
                "button",
                name="Закрыть ошибку",
                exact=True,
            )
        )

        self.error_close_button = self.error_message.get_by_role(
            "button",
            name="Закрыть ошибку",
            exact=True,
        )
        
    @allure.step("Открыть главную страницу")
    def open(self) -> Self:
        self.page.goto(self.URL)
        return self
        
    @allure.step("Вход в аккаунт администратора: {username}")
    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    @allure.step("Выход из аккаунта администратора")
    def logout(self) -> None:
        self.logout_button.click()
        
    @allure.step("Закрыть сообщение об ошибке авторизации")
    def close_login_error(self) -> None:
        self.error_close_button.click()