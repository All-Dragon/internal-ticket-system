from dataclasses import dataclass

import pytest

from e2e.config import e2e_config
from e2e.pages.ticket_page import TicketPage

@dataclass(frozen=True, slots=True)
class AdminCredentials:
    username: str
    password: str
    

@pytest.fixture(scope="session")
def admin_credentials() -> AdminCredentials:
    return AdminCredentials(
        username=e2e_config.admin_username,
        password=e2e_config.admin_password
    )
    
@pytest.fixture
def admin_ticket_page(
    ticket_page: TicketPage,
    admin_credentials: AdminCredentials
) -> TicketPage:
    ticket_page.open()
    ticket_page.login(
        username=admin_credentials.username,
        password=admin_credentials.password
    )
    
    return ticket_page