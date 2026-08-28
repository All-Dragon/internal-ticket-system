import allure
import pytest
from playwright.sync_api import expect
from uuid import uuid4

from e2e.models import (
    SortOrder,
    TicketPriority,
    TicketSortBy,
    TicketStatus,
)
from e2e.pages.ticket_page import TicketPage


@allure.feature("Заявки")
@allure.story("Фильтрация заявок")
@allure.title("Заявки фильтруются по статусу {selected_status}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
@pytest.mark.smoke
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
def test_tickets_can_be_filtered_by_status(
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
        f"Выбрать фильтр по статусу {selected_status.value}"
    ):
        admin_ticket_page.filters.filter_by_status(
            selected_status,
        )

        expect(
            admin_ticket_page.filters.status_field
        ).to_have_value(selected_status.value)

    with allure.step("Проверить отфильтрованные заявки"):
        for status, ticket in tickets.items():
            row = admin_ticket_page.ticket_table.row_by_id(
                ticket.id,
            )

            if status == selected_status:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()


@allure.feature("Заявки")
@allure.story("Фильтрация заявок")
@allure.title("Заявки фильтруются по приоритету {selected_priority}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "selected_priority",
    [
        TicketPriority.LOW,
        TicketPriority.NORMAL,
        TicketPriority.HIGH,
    ],
    ids=[
        "low",
        "normal",
        "high",
    ],
)
def test_tickets_can_be_filtered_by_priority(
    ticket_page: TicketPage,
    ticket_creator,
    selected_priority: TicketPriority,
):
    tickets = {
        priority: ticket_creator(priority=priority)
        for priority in TicketPriority
    }

    ticket_page.open()

    with allure.step(
        f"Выбрать фильтр по приоритету "
        f"{selected_priority.value}"
    ):
        ticket_page.filters.filter_by_priority(
            selected_priority,
        )

        expect(
            ticket_page.filters.priority_field
        ).to_have_value(selected_priority.value)

    with allure.step("Проверить отфильтрованные заявки"):
        for priority, ticket in tickets.items():
            row = ticket_page.ticket_table.row_by_id(
                ticket.id,
            )

            if priority == selected_priority:
                expect(row).to_be_visible()
            else:
                expect(row).not_to_be_visible()
                
@allure.feature("Заявки")
@allure.story("Сортировка заявок")
@allure.title(
    "Заявки сортируются по дате создания: {sort_order}"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_order",
    [
        SortOrder.ASC,
        SortOrder.DESC,
    ],
    ids=[
        "ascending",
        "descending",
    ],
)
def test_tickets_can_be_sorted_by_creation_date(
    ticket_page: TicketPage,
    ticket_creator,
    sort_order: SortOrder,
):
    marker = uuid4().hex[:8]
    
    older_ticket = ticket_creator(
        title=f"Сортировка {marker} первая"
    )
    
    newer_ticket = ticket_creator(
        title=f"Сортировка {marker} вторая"
    )
    
    expected_order = (
        [older_ticket, newer_ticket]
        if sort_order == SortOrder.ASC 
        else [newer_ticket, older_ticket]
    )
    
    ticket_page.open()
    
    with allure.step("Найти подготовленные заявки"):
        ticket_page.filters.search(marker)

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(2)
        
    with allure.step(
        f"Отсортировать заявки по дате: {sort_order.value}"
    ):
        ticket_page.filters.sort_by(
            TicketSortBy.CREATED_AT,
        )
        
        ticket_page.filters.set_sort_order(
            sort_order,
        )
        
        expect(
            ticket_page.filters.sort_by_field
        ).to_have_value(TicketSortBy.CREATED_AT.value)
        
        expect(
            ticket_page.filters.sort_order_field
        ).to_have_value(sort_order.value)
        
    with allure.step("Проверить порядок заявок"):
        for index, ticket in enumerate(expected_order):
            expect(
                ticket_page.ticket_table.rows.nth(index)
            ).to_contain_text(f"#{ticket.id}")
            
    
@allure.feature("Заявки")
@allure.story("Сортировка заявок")
@allure.title(
    "Заявки сортируются по приоритету: {sort_order}"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    (
        "sort_order",
        "expected_priorities",
    ),
    [
        (
            SortOrder.ASC,
            (
                TicketPriority.LOW,
                TicketPriority.NORMAL,
                TicketPriority.HIGH,
            ),
        ),
        (
            SortOrder.DESC,
            (
                TicketPriority.HIGH,
                TicketPriority.NORMAL,
                TicketPriority.LOW,
            ),
        ),
    ],
    ids=[
        "ascending",
        "descending",
    ],
)
def test_tickets_can_be_sorted_by_priority(
    ticket_page: TicketPage,
    ticket_creator,
    sort_order: SortOrder,
    expected_priorities: tuple[TicketPriority, ...],
):
    marker = uuid4().hex[:8]

    tickets = {
        priority: ticket_creator(
            title=f"Приоритет {marker} {priority.value}",
            priority=priority,
        )
        for priority in TicketPriority
    }

    ticket_page.open()

    with allure.step("Найти подготовленные заявки"):
        ticket_page.filters.search(marker)

        expect(
            ticket_page.ticket_table.rows
        ).to_have_count(3)

    with allure.step(
        f"Отсортировать заявки по приоритету: "
        f"{sort_order.value}"
    ):
        ticket_page.filters.sort_by(
            TicketSortBy.PRIORITY,
        )
        ticket_page.filters.set_sort_order(
            sort_order,
        )

        expect(
            ticket_page.filters.sort_by_field
        ).to_have_value(TicketSortBy.PRIORITY.value)

        expect(
            ticket_page.filters.sort_order_field
        ).to_have_value(sort_order.value)

    with allure.step("Проверить порядок заявок"):
        expected_tickets = [
            tickets[priority]
            for priority in expected_priorities
        ]

        for index, ticket in enumerate(expected_tickets):
            expect(
                ticket_page.ticket_table.rows.nth(index)
            ).to_contain_text(f"#{ticket.id}")
            
            
@allure.feature("Заявки")
@allure.story("Сортировка заявок")
@allure.title(
    "Заявки сортируются по статусу: {sort_order}"
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.parametrize(
    (
        "sort_order",
        "expected_statuses",
    ),
    [
        (
            SortOrder.ASC,
            (
                TicketStatus.NEW,
                TicketStatus.IN_PROGRESS,
                TicketStatus.DONE,
            ),
        ),
        (
            SortOrder.DESC,
            (
                TicketStatus.DONE,
                TicketStatus.IN_PROGRESS,
                TicketStatus.NEW,
            ),
        ),
    ],
    ids=[
        "ascending",
        "descending",
    ],
)
def test_tickets_can_be_sorted_by_status(
    admin_ticket_page: TicketPage,
    ticket_creator,
    sort_order: SortOrder,
    expected_statuses: tuple[TicketStatus, ...],
):
    marker = uuid4().hex[:8]
    
    tickets = {
        status: ticket_creator(
            title=f"Статус {marker} {status.value}",
            status=status,
        )
        for status in TicketStatus
    }
    
    admin_ticket_page.open()
    
    with allure.step("Найти подготовленные заявки"):
        admin_ticket_page.filters.search(marker)
        
        expect(
            admin_ticket_page.ticket_table.rows
            ).to_have_count(3)
        
    with allure.step(
        f"Отсортировать заявки по статусу: "
        f"{sort_order.value}"
    ):
        admin_ticket_page.filters.sort_by(
            TicketSortBy.STATUS,
        )
        
        admin_ticket_page.filters.set_sort_order(
            sort_order
        )
        
        expect(
            admin_ticket_page.filters.sort_by_field
        ).to_have_value(TicketSortBy.STATUS.value)
        
        expect(
            admin_ticket_page.filters.sort_order_field
        ).to_have_value(sort_order.value)
        
    with allure.step("Проверить порядок заявок"):
        expected_tickets = [
            tickets[status]
            for status in expected_statuses
        ]
        
        for index, ticket in enumerate(expected_tickets):
            expect(
                admin_ticket_page.ticket_table.rows.nth(index)
            ).to_contain_text(f"#{ticket.id}")
            
            
@allure.feature("Заявки")
@allure.story("Фильтрация заявок")
@allure.title("Кнопка сбрасывает фильтры и сортировку")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_filters_can_be_reset(
    ticket_page: TicketPage,
    ticket_creator,
):
    ticket = ticket_creator(
        priority=TicketPriority.LOW,
    )

    ticket_page.open()

    with allure.step("Применить фильтры и сортировку"):
        ticket_page.filters.search(ticket.title)

        expect(
            ticket_page.filters.search_field
        ).to_have_value(ticket.title)

        ticket_page.filters.filter_by_status(
            TicketStatus.DONE,
        )

        expect(
            ticket_page.filters.status_field
        ).to_have_value(TicketStatus.DONE.value)

        ticket_page.filters.filter_by_priority(
            TicketPriority.HIGH,
        )

        expect(
            ticket_page.filters.priority_field
        ).to_have_value(TicketPriority.HIGH.value)

        ticket_page.filters.sort_by(
            TicketSortBy.STATUS,
        )

        expect(
            ticket_page.filters.sort_by_field
        ).to_have_value(TicketSortBy.STATUS.value)

        ticket_page.filters.set_sort_order(
            SortOrder.ASC,
        )

        expect(
            ticket_page.filters.sort_order_field
        ).to_have_value(SortOrder.ASC.value)

        expect(
            ticket_page.ticket_table.row_by_id(ticket.id)
        ).not_to_be_visible()

    with allure.step("Сбросить фильтры"):
        ticket_page.filters.reset()

    with allure.step("Проверить значения по умолчанию"):
        expect(
            ticket_page.filters.search_field
        ).to_have_value("")

        expect(
            ticket_page.filters.status_field
        ).to_have_value("")

        expect(
            ticket_page.filters.priority_field
        ).to_have_value("")

        expect(
            ticket_page.filters.sort_by_field
        ).to_have_value(TicketSortBy.CREATED_AT.value)

        expect(
            ticket_page.filters.sort_order_field
        ).to_have_value(SortOrder.DESC.value)

    with allure.step("Проверить восстановление списка заявок"):
        expect(
            ticket_page.ticket_table.row_by_id(ticket.id)
        ).to_be_visible()
        
        
@allure.feature("Заявки")
@allure.story("Фильтрация заявок")
@allure.title("Несколько фильтров применяются одновременно")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.e2e
@pytest.mark.regression
def test_multiple_filters_can_be_applied_together(
    admin_ticket_page: TicketPage,
    ticket_creator,
):
    marker = uuid4().hex[:8]

    matching_ticket = ticket_creator(
        title=f"Комбинация {marker} подходящая",
        priority=TicketPriority.HIGH,
        status=TicketStatus.DONE,
    )

    wrong_priority_ticket = ticket_creator(
        title=f"Комбинация {marker} другой приоритет",
        priority=TicketPriority.LOW,
        status=TicketStatus.DONE,
    )

    wrong_status_ticket = ticket_creator(
        title=f"Комбинация {marker} другой статус",
        priority=TicketPriority.HIGH,
        status=TicketStatus.NEW,
    )

    wrong_search_ticket = ticket_creator(
        title="Заявка вне поискового запроса",
        priority=TicketPriority.HIGH,
        status=TicketStatus.DONE,
    )

    admin_ticket_page.open()

    with allure.step("Применить несколько фильтров"):
        admin_ticket_page.filters.search(marker)
        admin_ticket_page.filters.filter_by_status(
            TicketStatus.DONE,
        )
        admin_ticket_page.filters.filter_by_priority(
            TicketPriority.HIGH,
        )

        expect(
            admin_ticket_page.filters.search_field
        ).to_have_value(marker)

        expect(
            admin_ticket_page.filters.status_field
        ).to_have_value(TicketStatus.DONE.value)

        expect(
            admin_ticket_page.filters.priority_field
        ).to_have_value(TicketPriority.HIGH.value)

    with allure.step(
        "Проверить заявку, соответствующую всем фильтрам"
    ):
        expect(
            admin_ticket_page.ticket_table.row_by_id(
                matching_ticket.id,
            )
        ).to_be_visible()

    with allure.step(
        "Проверить заявки, не соответствующие фильтрам"
    ):
        for ticket in (
            wrong_priority_ticket,
            wrong_status_ticket,
            wrong_search_ticket,
        ):
            expect(
                admin_ticket_page.ticket_table.row_by_id(
                    ticket.id,
                )
            ).not_to_be_visible()