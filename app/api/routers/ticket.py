from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas import (
    TicketCreate,
    TicketListParams,
    TicketListResponse,
    TicketRead,
    TicketStatusUpdate,
)
from app.services import TicketService
from app.core.JWT.admin_auth import require_admin

ticket_router  = APIRouter(
    prefix="/tickets", 
    tags=["tickets"]
)

@ticket_router.get('', response_model=TicketListResponse)
async def get_tickets(
    params: TicketListParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    return await TicketService.get_list(session=session, params=params)

@ticket_router.get("/{id}", response_model=TicketRead)
async def get_ticket_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    ticket = await TicketService.get_by_id(session=session, id=id)
    return TicketRead.model_validate(ticket)

@ticket_router.post(
        '', 
        status_code=status.HTTP_201_CREATED,
        response_model=TicketRead
)
async def create(
    data: TicketCreate,
    session: AsyncSession = Depends(get_async_session)
):
    ticket = await TicketService.create(session=session, data=data)
    return TicketRead.model_validate(ticket)

@ticket_router.patch("/{id}/status", response_model=TicketRead)
async def update_ticket_status(
    id: int,
    data: TicketStatusUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    ticket = await TicketService.update_status(session=session, id=id, data=data)
    return TicketRead.model_validate(ticket)

@ticket_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    current_admin = Depends(require_admin)
):
    await TicketService.delete(session=session, id=id)
