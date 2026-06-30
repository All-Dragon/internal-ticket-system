import asyncio
import logging
import os

from sqlalchemy import func, select

from app.core.logging_config import setup_logging
from app.db.database import AsyncSessionLocal
from app.db.enum import TicketPriority, TicketStatus
from app.db.models import Ticket

logger = logging.getLogger(__name__)

DEMO_TICKETS = [
    {
        "title": "Починить принтер в офисе 101",
        "description": "Принтер зажевывает бумагу и выдает ошибку при печати документов.",
        "status": TicketStatus.new,
        "priority": TicketPriority.high,
    },
    {
        "title": "Не работает интернет",
        "description": "Нет подключения к сети после перезагрузки роутера утром.",
        "status": TicketStatus.new,
        "priority": TicketPriority.normal,
    },
    {
        "title": "Добавить сотрудника в систему",
        "description": "Нужно создать учетную запись для нового сотрудника отдела продаж.",
        "status": TicketStatus.new,
        "priority": TicketPriority.low,
    },
    {
        "title": "Обновить антивирус",
        "description": "Требуется обновление лицензии и проверка рабочих станций.",
        "status": TicketStatus.in_progress,
        "priority": TicketPriority.normal,
    },
    {
        "title": "Настроить доступ к VPN",
        "description": "Доступ к VPN настроен и проверен на рабочем ноутбуке.",
        "status": TicketStatus.done,
        "priority": TicketPriority.high,
    },
]


def _is_demo_seed_enabled() -> bool:
    return os.getenv("SEED_DEMO_DATA", "true").lower() not in {"0", "false", "no"}


async def seed_demo_tickets() -> None:
    if not _is_demo_seed_enabled():
        logger.info("Заполнение демо-заявками отключено")
        return

    async with AsyncSessionLocal() as session:
        total = await session.scalar(select(func.count(Ticket.id)))

        if total:
            logger.info("Демо-заявки не добавлены: в базе уже есть заявки")
            return

        session.add_all(Ticket(**ticket_data) for ticket_data in DEMO_TICKETS)
        await session.commit()

        logger.info("Добавлены демо-заявки: %s", len(DEMO_TICKETS))


def main() -> None:
    setup_logging()
    asyncio.run(seed_demo_tickets())


if __name__ == "__main__":
    main()
