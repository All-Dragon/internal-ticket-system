import allure
import pytest
from playwright.sync_api import expect

from e2e.models import TicketStatus, TicketPriority
from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Быстрые фильтры")
@allure.title(
    "Быстрый фильтр отображает заявки со статусом {selected_status}"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "selected_status",
    [
        TicketStatus.NEW,
        TicketStatus.IN_PROGRESS,
        TicketStatus.DONE,
    ],
    ids=[
        "new",
        "in-progress",
        "done",
    ],
)
def test_quick_filter_filters_tickets_by_status(
    admin_ticket_page: TicketPage,
    ticket_creator,
    selected_status: TicketStatus,
):
    tickets = {
        status: ticket_creator(status=status)
        for status in TicketStatus
    }

    admin_ticket_page.open()

    with allure.step(
        f"Применить быстрый фильтр {selected_status.value}"
    ):
        admin_ticket_page.quick_filters.filter_by_status(
            selected_status,
        )

    with allure.step("Проверить состояние быстрых фильтров"):
        expect(
            admin_ticket_page.quick_filters.all_tickets_button
        ).to_have_attribute("aria-pressed", "false")

        for status in TicketStatus:
            expected_state = (
                "true"
                if status == selected_status
                else "false"
            )

            expect(
                admin_ticket_page.quick_filters.status_button(
                    status,
                )
            ).to_have_attribute(
                "aria-pressed",
                expected_state,
            )

        expect(
            admin_ticket_page.quick_filters.high_priority_button
        ).to_have_attribute("aria-pressed", "false")

    with allure.step(
        "Проверить синхронизацию с обычным фильтром"
    ):
        expect(
            admin_ticket_page.filters.status_field
        ).to_have_value(selected_status.value)

        expect(
            admin_ticket_page.filters.priority_field
        ).to_have_value("")

    with allure.step("Проверить заявки в таблице"):
        for status, ticket in tickets.items():
            row = admin_ticket_page.ticket_table.row_by_id(
                ticket.id,
            )

            if status == selected_status:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()
                
@allure.feature("Заявки")
@allure.story("Быстрые фильтры")
@allure.title(
    "Быстрый фильтр отображает заявки высокого приоритета"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_quick_filter_filters_high_priority_tickets(
    ticket_page: TicketPage,
    ticket_creator,
):
    tickets = {
        priority: ticket_creator(priority=priority)
        for priority in TicketPriority 
    }
    
    ticket_page.open()
    
    with allure.step(
        "Применить фильтр высокого приоритета"
    ):
        ticket_page.quick_filters.filter_by_high_priority()
        
    with allure.step("Проверить состояние быстрых фильтров"):
        expect(
            ticket_page.quick_filters.high_priority_button
            ).to_have_attribute("aria-pressed", "true")
        
        expect(
            ticket_page.quick_filters.all_tickets_button
        ).to_have_attribute("aria-pressed", "false")
        
        for status in TicketStatus:
            expect(
                ticket_page.quick_filters.status_button(status)
            ).to_have_attribute("aria-pressed", "false")
            
    with allure.step(
        "Проверить синхронизацию с обычными фильтрами"
    ):
        expect(
            ticket_page.filters.priority_field
        ).to_have_value(TicketPriority.HIGH.value)
        
        expect(
            ticket_page.filters.status_field
        ).to_have_value("")
        
    with allure.step("Проверить заявки в таблице"):
        for priority, ticket in tickets.items():
            row = ticket_page.ticket_table.row_by_id(
                ticket.id
            )
            
            if priority == TicketPriority.HIGH:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()
                
@allure.feature("Заявки")
@allure.story("Быстрые фильтры")
@allure.title(
    "Кнопка «Все заявки» отключает быстрый фильтр"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_all_tickets_button_resets_quick_filter(
    ticket_page: TicketPage,
    ticket_creator,
):
    tickets = {
        priority: ticket_creator(priority=priority)
        for priority in TicketPriority
    }

    ticket_page.open()

    with allure.step(
        "Применить фильтр высокого приоритета"
    ):
        ticket_page.quick_filters.filter_by_high_priority()

        expect(
            ticket_page.quick_filters.high_priority_button
        ).to_have_attribute("aria-pressed", "true")

        expect(
            ticket_page.quick_filters.all_tickets_button
        ).to_have_attribute("aria-pressed", "false")

        for priority, ticket in tickets.items():
            row = ticket_page.ticket_table.row_by_id(
                ticket.id,
            )

            if priority == TicketPriority.HIGH:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()

    with allure.step("Нажать кнопку «Все заявки»"):
        ticket_page.quick_filters.show_all_tickets()

    with allure.step("Проверить состояние фильтров"):
        expect(
            ticket_page.quick_filters.all_tickets_button
        ).to_have_attribute("aria-pressed", "true")

        expect(
            ticket_page.quick_filters.high_priority_button
        ).to_have_attribute("aria-pressed", "false")

        for status in TicketStatus:
            expect(
                ticket_page.quick_filters.status_button(status)
            ).to_have_attribute("aria-pressed", "false")

        expect(
            ticket_page.filters.status_field
        ).to_have_value("")

        expect(
            ticket_page.filters.priority_field
        ).to_have_value("")

    with allure.step("Проверить отображение всех заявок"):
        for ticket in tickets.values():
            expect(
                ticket_page.ticket_table.row_by_id(ticket.id)
            ).to_be_visible()
            
            
@allure.feature("Заявки")
@allure.story("Быстрые фильтры")
@allure.title(
    "Кнопка «Сбросить фильтры» отключает быстрый фильтр"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_reset_button_clears_quick_filter(
    ticket_page: TicketPage,
    ticket_creator,
):
    tickets = {
        priority: ticket_creator(priority=priority)
        for priority in TicketPriority
    }

    ticket_page.open()

    with allure.step(
        "Применить быстрый фильтр высокого приоритета"
    ):
        ticket_page.quick_filters.filter_by_high_priority()

        expect(
            ticket_page.quick_filters.high_priority_button
        ).to_have_attribute("aria-pressed", "true")

        expect(
            ticket_page.filters.priority_field
        ).to_have_value(TicketPriority.HIGH.value)

        for priority, ticket in tickets.items():
            row = ticket_page.ticket_table.row_by_id(
                ticket.id,
            )

            if priority == TicketPriority.HIGH:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()

    with allure.step("Нажать кнопку «Сбросить фильтры»"):
        ticket_page.filters.reset()

    with allure.step("Проверить состояние фильтров"):
        expect(
            ticket_page.quick_filters.all_tickets_button
        ).to_have_attribute("aria-pressed", "true")

        expect(
            ticket_page.quick_filters.high_priority_button
        ).to_have_attribute("aria-pressed", "false")

        for status in TicketStatus:
            expect(
                ticket_page.quick_filters.status_button(status)
            ).to_have_attribute("aria-pressed", "false")

        expect(
            ticket_page.filters.priority_field
        ).to_have_value("")

        expect(
            ticket_page.filters.status_field
        ).to_have_value("")

    with allure.step("Проверить отображение всех заявок"):
        for ticket in tickets.values():
            expect(
                ticket_page.ticket_table.row_by_id(ticket.id)
            ).to_be_visible()