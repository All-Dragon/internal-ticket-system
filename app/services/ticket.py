import logging
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enum import TicketStatus
from app.db.models import Ticket
from app.repositories import TicketListCriteria, TicketRepository
from app.schemas import (
    TicketCreate,
    TicketListParams,
    TicketListResponse,
    TicketStatusUpdate,
)

logger = logging.getLogger(__name__)


class TicketService:
    @staticmethod
    async def get_list(
        session: AsyncSession,
        params: TicketListParams,
    ):
        logger.info(
            "Получение списка заявок: status=%s priority=%s search=%s sort_by=%s sort_order=%s page=%s page_size=%s",
            params.status,
            params.priority,
            params.search,
            params.sort_by,
            params.sort_order,
            params.page,
            params.page_size,
        )

        criteria = TicketListCriteria(
            status=params.status,
            priority=params.priority,
            search=params.search,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
            offset=(params.page - 1) * params.page_size,
            limit=params.page_size,
        )

        try:
            tickets, total = await TicketRepository.get_list(
                session=session,
                criteria=criteria,
            )
        except Exception:
            logger.exception("Ошибка при получении списка заявок")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка сервера при получении списка заявок",
            )

        pages = ceil(total / params.page_size) if total else 0

        return TicketListResponse(
            items=tickets,
            total=total,
            page=params.page,
            page_size=params.page_size,
            pages=pages,
        )
    
    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        id: int,
    ):
        logger.info("Получение заявки по id %s", id)
        ticket = await TicketRepository.get_by_id(session=session, ticket_id=id)
        if not ticket:
            logger.warning("Заявка с id %s не найдена", id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка с таким id не найдена",
            )
        return ticket
    
    @staticmethod
    async def create(
        session: AsyncSession,
        data: TicketCreate,
    ):
        logger.info("Создание заявки с title=%s priority=%s", data.title, data.priority)

        try:
            return await TicketRepository.create(
                session=session,
                data=data,
            )
        except Exception:
            logger.exception("Ошибка при создании заявки с title=%s", data.title)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка сервера при создании заявки",
            )
        
    @staticmethod
    async def update_status(
        session: AsyncSession,
        id: int,
        data: TicketStatusUpdate,
    ):
        logger.info("Изменение статуса заявки id=%s на %s", id, data.status)

        ticket = await TicketService.get_by_id(session=session, id=id)

        if ticket.status == TicketStatus.done:
            logger.warning("Попытка изменить заявку в статусе done: id=%s", id)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Заявку в статусе done нельзя редактировать",
            )
        
        try:
            return await TicketRepository.update_status(
                session=session,
                ticket=ticket,
                status=data.status,
            )
        
        except Exception:
            logger.exception("Ошибка при изменении статуса заявки id=%s", id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка сервера при изменении статуса заявки",
            )
        
    @staticmethod
    async def delete(
        session: AsyncSession,
        id: int,
    ) -> None:
        logger.info("Удаление заявки id=%s", id)

        ticket = await TicketService.get_by_id(session=session, id=id)

        if ticket.status == TicketStatus.done:
            logger.warning("Попытка удалить заявку в статусе done: id=%s", id)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Заявку в статусе done нельзя удалить",
            )

        try:
            await TicketRepository.delete(session=session, ticket=ticket)
        except Exception:
            logger.exception("Ошибка при удалении заявки id=%s", id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка сервера при удалении заявки",
            )
