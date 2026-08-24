from dataclasses import dataclass
from typing import Literal
from uuid import uuid4

import pytest


TicketPriority = Literal["low", "normal", "high"]

@dataclass(frozen=True, slots=True)
class TicketData:
    title: str
    description: str
    priority: TicketPriority
    
@pytest.fixture
def ticket_data_factory():
    def build_ticket(
        title: str | None = None,
        description: str | None = None,
        priority: TicketPriority = "normal",
    ) -> TicketData:
        unique_id = uuid4().hex[:8]

        return TicketData(
            title=title or f"E2E заявка {unique_id}",
            description=description or f"Описание E2E заявки {unique_id}",
            priority=priority,
        )

    return build_ticket