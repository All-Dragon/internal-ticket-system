import allure
import pytest
from playwright.sync_api import Page

from e2e.config import e2e_config

from e2e.pages.ticket_page import TicketPage

from e2e.fixtures import (
    admin_credentials,
    admin_ticket_page,
    ticket_data_factory,
)

__all__ = [
    "admin_credentials",
    "admin_ticket_page",
    "ticket_data_factory",
]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": (
            browser_context_args.get("base_url")
            or e2e_config.base_url
        ),
        "locale": "ru-RU",
        "timezone_id": "UTC",
        "viewport": {
            "width": 1440,
            "height": 900,
        },
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page: Page | None = item.funcargs.get("page")

    if page is None or page.is_closed():
        return

    try:
        screenshot = page.screenshot(full_page=True)
    except Exception as screenshot_error:
        allure.attach(
            str(screenshot_error),
            name="Screenshot error",
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    allure.attach(
        screenshot,
        name="Failure screenshot",
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        page.url,
        name="Page URL",
        attachment_type=allure.attachment_type.TEXT,
    )
    
    
@pytest.fixture
def ticket_page(page: Page) -> TicketPage:
    return TicketPage(page)