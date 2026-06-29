import { useEffect, useState } from "react";

import {
  deleteTicket,
  getTickets,
  updateTicketStatus,
} from "../api/ticket";
import { DEFAULT_FILTERS } from "../types/ticketPage";

import type { ChangeEvent } from "react";
import type { ApiError } from "../types/api";
import type {
  Ticket,
  TicketListParams,
  TicketStatus,
} from "../types/ticket";
import type { TicketFilters } from "../types/ticketPage";

function buildParams(filters: TicketFilters): TicketListParams {
  return {
    status: filters.status || undefined,
    priority: filters.priority || undefined,
    search: filters.search.trim() || undefined,
    sort_by: filters.sort_by,
    sort_order: filters.sort_order,
    page: filters.page,
    page_size: filters.page_size,
  };
}

function getErrorMessage(err: unknown, fallback: string): string {
  const apiError = err instanceof Error ? (err as ApiError) : null;
  return apiError?.message ?? fallback;
}

function useTicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [filters, setFilters] = useState<TicketFilters>(DEFAULT_FILTERS);

  const [total, setTotal] = useState<number>(0);
  const [pages, setPages] = useState<number>(0);

  const [loading, setLoading] = useState<boolean>(true);
  const [updatingTicketId, setUpdatingTicketId] = useState<number | null>(null);
  const [deletingTicketId, setDeletingTicketId] = useState<number | null>(null);
  const [error, setError] = useState<string>("");

  async function loadTickets(
    nextFilters: TicketFilters = filters,
  ): Promise<void> {
    setLoading(true);
    setError("");

    try {
      const data = await getTickets(buildParams(nextFilters));

      setTickets(data.items);
      setTotal(data.total);
      setPages(data.pages);
      setFilters({
        ...nextFilters,
        page: data.page,
        page_size: data.page_size,
      });
    } catch (err) {
      setTickets([]);
      setTotal(0);
      setPages(0);
      setError(getErrorMessage(err, "Не удалось загрузить заявки"));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialTickets(): Promise<void> {
      try {
        const data = await getTickets(buildParams(DEFAULT_FILTERS));

        if (cancelled) {
          return;
        }

        setTickets(data.items);
        setTotal(data.total);
        setPages(data.pages);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setTickets([]);
        setTotal(0);
        setPages(0);
        setError(getErrorMessage(err, "Не удалось загрузить заявки"));
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadInitialTickets();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleStatusChange(
    id: number,
    status: TicketStatus,
  ): Promise<void> {
    try {
      setUpdatingTicketId(id);
      setError("");

      await updateTicketStatus(id, status);
      await loadTickets(filters);
    } catch (err) {
      setError(getErrorMessage(err, "Не удалось изменить статус"));
    } finally {
      setUpdatingTicketId(null);
    }
  }

  async function handleDeleteTicket(id: number): Promise<void> {
    try {
      setDeletingTicketId(id);
      setError("");

      await deleteTicket(id);
      await loadTickets(filters);
    } catch (err) {
      setError(getErrorMessage(err, "Не удалось удалить заявку"));
    } finally {
      setDeletingTicketId(null);
    }
  }

  async function handleFilterChange(
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ): Promise<void> {
    const { name, value } = event.target;

    const nextFilters: TicketFilters = {
      ...filters,
      [name]: value,
      page: 1,
    };

    setFilters(nextFilters);
    await loadTickets(nextFilters);
  }

  async function handlePageChange(page: number): Promise<void> {
    const nextFilters: TicketFilters = {
      ...filters,
      page,
    };

    setFilters(nextFilters);
    await loadTickets(nextFilters);
  }

  async function handleResetFilters(): Promise<void> {
    setFilters(DEFAULT_FILTERS);
    await loadTickets(DEFAULT_FILTERS);
  }

  return {
    tickets,
    filters,
    total,
    pages,
    loading,
    updatingTicketId,
    deletingTicketId,
    error,
    loadTickets,
    handleStatusChange,
    handleDeleteTicket,
    handleFilterChange,
    handlePageChange,
    handleResetFilters,
  };
}

export default useTicketsPage;
