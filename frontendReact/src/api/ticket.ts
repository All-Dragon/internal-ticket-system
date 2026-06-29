import { apiUrl } from "./config";
import { authFetch } from "./authFetch";

import type {
  Ticket,
  TicketCreate,
  TicketListParams,
  TicketListResponse,
  TicketStatus,
} from "../types/ticket";

function buildTicketQuery(params: TicketListParams = {}): string {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });

  const query = searchParams.toString();

  return query ? `?${query}` : "";
}

export async function getTickets(
  params: TicketListParams = {},
): Promise<TicketListResponse> {
  const query = buildTicketQuery(params);

  return authFetch<TicketListResponse>(apiUrl(`/tickets${query}`));
}

export async function createTicket(data: TicketCreate): Promise<Ticket> {
  return authFetch<Ticket>(apiUrl("/tickets"), {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateTicketStatus(
  id: number,
  status: TicketStatus,
): Promise<Ticket> {
  return authFetch<Ticket>(apiUrl(`/tickets/${id}/status`), {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

export async function deleteTicket(id: number): Promise<void> {
  return authFetch<void>(apiUrl(`/tickets/${id}`), {
    method: "DELETE",
  });
}
