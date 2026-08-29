from typing import Literal
from uuid import uuid4

import allure
import pytest
from playwright.sync_api import expect

from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Поиск заявок")
@allure.title(
    "Заявка находится по полю {searched_field}"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "searched_field",
    [
        "title",
        "description",
    ],
    ids=[
        "title",
        "description",
    ],
)
def test_ticket_can_be_found_by_text_field(
    ticket_page: TicketPage,
    ticket_creator,
    searched_field: Literal["title", "description"],
):
    marker = uuid4().hex[:8]

    matching_ticket = ticket_creator(
        title=(
            f"Поисковый заголовок {marker}"
            if searched_field == "title"
            else "Заявка для поиска по описанию"
        ),
        description=(
            f"Поисковое описание {marker}"
            if searched_field == "description"
            else "Описание без поискового маркера"
        ),
    )
    
    unrelated_ticket = ticket_creator(
        title="Посторонняя заявка",
        description="Постороннее описание",
    )
    
    ticket_page.open()
    
    with allure.step(
        f"Выполнить поиск по полю {searched_field}"
    ):
        ticket_page.filters.search(marker)
        
        expect(
            ticket_page.filters.search_field
        ).to_have_value(marker)
    
    
    with allure.step("Проверить результаты поиска"):
        expect(
            ticket_page.ticket_table.row_by_id(matching_ticket.id)
        ).to_have_count(1)
        
        expect(
            ticket_page.ticket_table.row_by_id(matching_ticket.id)
        ).to_be_visible()
        
        expect(
            ticket_page.ticket_table.row_by_id(
                unrelated_ticket.id,
            )
        ).not_to_be_visible()
        
@allure.feature("Заявки")
@allure.story("Поиск заявок")
@allure.title("Для несуществующего запроса показана пустая выдача")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_search_displays_empty_state(
    ticket_page: TicketPage,
):
    search_query = f"missing-{uuid4().hex}"

    ticket_page.open()

    with allure.step("Выполнить поиск несуществующей заявки"):
        ticket_page.filters.search(search_query)

        expect(
            ticket_page.filters.search_field
        ).to_have_value(search_query)

    with allure.step("Проверить состояние пустой выдачи"):
        expect(
            ticket_page.ticket_table.empty_tickets_state
        ).to_be_visible()

        expect(
            ticket_page.ticket_table.empty_tickets_state
        ).to_contain_text(
            "Попробуйте изменить параметры поиска."
        )

        expect(
            ticket_page.ticket_table.root
        ).not_to_be_visible()