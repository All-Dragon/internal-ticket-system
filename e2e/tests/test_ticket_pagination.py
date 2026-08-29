from uuid import uuid4

import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Пагинация")
@allure.title("Пользователь может переходить между страницами")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_user_can_navigate_between_ticket_pages(
    ticket_page: TicketPage,
    ticket_creator,
):
    marker = uuid4().hex[:8]

    tickets = [
        ticket_creator(
            title=f"Пагинация {marker} заявка {number}",
        )
        for number in range(1, 7)
    ]

    oldest_ticket = tickets[0]
    newest_ticket = tickets[-1]

    ticket_page.open()

    with allure.step("Найти подготовленные заявки"):
        ticket_page.filters.search(marker)

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(6)

    with allure.step("Установить пять заявок на странице"):
        ticket_page.ticket_table.set_page_size(5)

        expect(
            ticket_page.ticket_table.page_size_field
        ).to_have_value("5")

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(5)

    with allure.step("Проверить первую страницу"):
        expect(
            ticket_page.ticket_table.previous_page_button
        ).to_be_disabled()

        expect(
            ticket_page.ticket_table.next_page_button
        ).to_be_enabled()

        expect(
            ticket_page.ticket_table.page_button(1)
        ).to_have_attribute("aria-current", "page")

        expect(
            ticket_page.ticket_table.pagination_summary
        ).to_have_text("Показано 1-5 из 6 заявок")

        expect(
            ticket_page.ticket_table.row_by_id(
                newest_ticket.id,
            )
        ).to_be_visible()

        expect(
            ticket_page.ticket_table.row_by_id(
                oldest_ticket.id,
            )
        ).not_to_be_visible()

    with allure.step("Перейти на вторую страницу"):
        ticket_page.ticket_table.go_to_next_page()

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(1)

    with allure.step("Проверить вторую страницу"):
        expect(
            ticket_page.ticket_table.previous_page_button
        ).to_be_enabled()

        expect(
            ticket_page.ticket_table.next_page_button
        ).to_be_disabled()

        expect(
            ticket_page.ticket_table.page_button(2)
        ).to_have_attribute("aria-current", "page")

        expect(
            ticket_page.ticket_table.pagination_summary
        ).to_have_text("Показано 6-6 из 6 заявок")

        expect(
            ticket_page.ticket_table.row_by_id(
                oldest_ticket.id,
            )
        ).to_be_visible()

        expect(
            ticket_page.ticket_table.row_by_id(
                newest_ticket.id,
            )
        ).not_to_be_visible()

    with allure.step("Вернуться на первую страницу"):
        ticket_page.ticket_table.go_to_previous_page()

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(5)

        expect(
            ticket_page.ticket_table.page_button(1)
        ).to_have_attribute("aria-current", "page")

        expect(
            ticket_page.ticket_table.row_by_id(
                newest_ticket.id,
            )
        ).to_be_visible()
        
        
@allure.feature("Заявки")
@allure.story("Пагинация")
@allure.title("Пользователь может изменить количество заявок на странице")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_user_can_change_ticket_page_size(
    ticket_page: TicketPage,
    ticket_creator,
):
    marker = uuid4().hex

    tickets = [
        ticket_creator(
            title=f"Размер страницы {marker} заявка {number}",
        )
        for number in range(1, 7)
    ]

    ticket_page.open()

    with allure.step("Найти подготовленные заявки"):
        ticket_page.filters.search(marker)

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(6)

    with allure.step("Установить пять заявок на странице"):
        ticket_page.ticket_table.set_page_size(5)

        expect(
            ticket_page.ticket_table.page_size_field
        ).to_have_value("5")

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(5)

        expect(
            ticket_page.ticket_table.pagination_summary
        ).to_have_text("Показано 1-5 из 6 заявок")

        expect(
            ticket_page.ticket_table.next_page_button
        ).to_be_enabled()

    with allure.step("Установить десять заявок на странице"):
        ticket_page.ticket_table.set_page_size(10)

        expect(
            ticket_page.ticket_table.page_size_field
        ).to_have_value("10")

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(6)

        expect(
            ticket_page.ticket_table.pagination_summary
        ).to_have_text("Показано 1-6 из 6 заявок")

        expect(
            ticket_page.ticket_table.next_page_button
        ).to_be_disabled()

    with allure.step("Проверить отображение всех заявок"):
        for ticket in tickets:
            expect(
                ticket_page.ticket_table.row_by_id(ticket.id)
            ).to_be_visible()