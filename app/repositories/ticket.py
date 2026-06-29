from sqlalchemy import asc, case, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.enum import SortOrder, TicketPriority, TicketSortBy, TicketStatus
from app.db.models import Ticket
from app.repositories.ticket_criteria import TicketListCriteria
from app.schemas import TicketCreate, TicketUpdate


class TicketRepository:
    @staticmethod
    async def get_by_id(session: AsyncSession, ticket_id: int) -> Ticket | None:
        return await session.scalar(select(Ticket).where(Ticket.id == ticket_id))

    @staticmethod
    async def create(session: AsyncSession, data: TicketCreate) -> Ticket:
        ticket = Ticket(
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=TicketStatus.new,
        )
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        return ticket

    @staticmethod
    async def get_list(
        session: AsyncSession,
        criteria: TicketListCriteria,
    ) -> tuple[list[Ticket], int]:
        query = select(Ticket)
        count_query = select(func.count(Ticket.id))

        filters = TicketRepository._build_filters(criteria)

        if filters:
            query = query.where(*filters)
            count_query = count_query.where(*filters)

        order_column = TicketRepository._get_order_column(criteria.sort_by)
        order_expression = (
            asc(order_column)
            if criteria.sort_order == SortOrder.asc
            else desc(order_column)
        )

        total = await session.scalar(count_query)
        result = await session.scalars(
            query.order_by(order_expression)
            .offset(criteria.offset)
            .limit(criteria.limit)
        )

        return list(result.all()), total or 0

    @staticmethod
    async def update(
        session: AsyncSession,
        ticket: Ticket,
        data: TicketUpdate
    ) -> Ticket:
        ticket.title = data.title
        ticket.description = data.description
        ticket.priority = data.priority

        await session.commit()
        await session.refresh(ticket)
        return ticket

    @staticmethod
    async def update_status(
        session: AsyncSession,
        ticket: Ticket,
        status: TicketStatus,
    ) -> Ticket:
        ticket.status = status
        await session.commit()
        await session.refresh(ticket)
        return ticket

    @staticmethod
    async def delete(session: AsyncSession, ticket: Ticket) -> None:
        await session.delete(ticket)
        await session.commit()

    @staticmethod
    def _build_filters(criteria: TicketListCriteria):
        filters = []

        if criteria.status is not None:
            filters.append(Ticket.status == criteria.status)

        if criteria.priority is not None:
            filters.append(Ticket.priority == criteria.priority)

        if criteria.search is not None:
            search_pattern = f"%{criteria.search.casefold()}%"
            filters.append(
                or_(
                    func.casefold(Ticket.title).like(search_pattern),
                    func.casefold(Ticket.description).like(search_pattern),
                )
            )

        return filters

    @staticmethod
    def _get_order_column(sort_by: TicketSortBy):
        if sort_by == TicketSortBy.priority:
            return case(
                (Ticket.priority == TicketPriority.low, 1),
                (Ticket.priority == TicketPriority.normal, 2),
                (Ticket.priority == TicketPriority.high, 3),
                else_=2,
            )

        if sort_by == TicketSortBy.status:
            return case(
                (Ticket.status == TicketStatus.new, 1),
                (Ticket.status == TicketStatus.in_progress, 2),
                (Ticket.status == TicketStatus.done, 3),
                else_=1,
            )

        return Ticket.created_at
