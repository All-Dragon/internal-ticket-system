import { useState } from "react";

import AdminLoginForm from "../components/AdminLoginForm";
import TicketCreateForm from "../components/TicketCreateForm";
import TicketDashboardPanel from "../components/TicketDashboardPanel";
import TicketDeleteConfirmModal from "../components/TicketDeleteConfirmModal";
import TicketDetailsModal from "../components/TicketDetailsModal";
import TicketEditModal from "../components/TicketEditModal";
import TicketFilters from "../components/TicketFilters";
import SystemInfoModal from "../components/SystemInfoModal";
import TicketStatusPanel from "../components/TicketStatusPanel";
import TicketTable from "../components/TicketTable";

import useAdminAuth from "../hooks/useAdminAuth";
import useTicketsPage from "../hooks/useTicketsPage";

import type { Ticket } from "../types/ticket";

function TicketPage() {
  const adminAuth = useAdminAuth();
  const ticketsPage = useTicketsPage();

  async function handleTicketCreated(): Promise<void> {
    await ticketsPage.loadTickets({
      ...ticketsPage.filters,
      page: 1,
    });
  }

  const [editingTicket, setEditingTicket] = useState<Ticket | null>(null);
  const [viewingTicket, setViewingTicket] = useState<Ticket | null>(null);
  const [isSystemInfoOpen, setIsSystemInfoOpen] = useState<boolean>(false);
  const [deletingTicket, setDeletingTicket] = useState<Ticket | null>(null);

  function handleViewTicket(ticket: Ticket): void {
    setViewingTicket(ticket);
  }

  function handleViewClose(): void {
    setViewingTicket(null);
  }

  function handleEditTicket(ticket: Ticket): void {
    if (ticket.status === "done") {
      return;
    }

    setEditingTicket(ticket);
  }

  function handleEditClose(): void {
    setEditingTicket(null);
  }

  async function handleTicketUpdated(): Promise<void> {
    await ticketsPage.loadTickets(ticketsPage.filters);
    setEditingTicket(null);
  }

  function handleDetailsEdit(ticket: Ticket): void {
    setViewingTicket(null);
    handleEditTicket(ticket);
  }

  function handleSystemInfoOpen(): void {
    setIsSystemInfoOpen(true);
  }

  function handleSystemInfoClose(): void {
    setIsSystemInfoOpen(false);
  }

  function handleDeleteRequest(ticket: Ticket): void {
    if (ticket.status === "done") {
      return;
    }

    setViewingTicket(null);
    setDeletingTicket(ticket);
  }

  function handleDeleteCancel(): void {
    setDeletingTicket(null);
  }

  async function handleDeleteConfirm(id: number): Promise<void> {
    await ticketsPage.handleDeleteTicket(id);
    setDeletingTicket(null);
    setViewingTicket(null);
  }

  const isTicketsEmpty = !ticketsPage.loading && ticketsPage.tickets.length === 0;
  const isAllTicketsActive =
    ticketsPage.filters.status === "" &&
    ticketsPage.filters.priority === "" &&
    ticketsPage.filters.search.trim() === "";

  return (
    <main className="appPage">
      <header className="appHeader">
        <h1 className="appTitle">Внутренние заявки</h1>

        <button
          className="systemInfoButton"
          type="button"
          onClick={handleSystemInfoOpen}
        >
          О системе
        </button>

        <AdminLoginForm
          formData={adminAuth.formData}
          loading={adminAuth.loading}
          error={adminAuth.error}
          isAdmin={adminAuth.isAdmin}
          onChange={adminAuth.handleChange}
          onSubmit={adminAuth.handleSubmit}
          onLogout={adminAuth.handleLogout}
          onErrorClose={adminAuth.handleErrorClose}
        />
      </header>

      <section className="topGrid">
        <TicketCreateForm onCreated={handleTicketCreated} />

        <TicketDashboardPanel
          tickets={ticketsPage.tickets}
          total={ticketsPage.total}
          activeQuickFilter={ticketsPage.activeQuickFilter}
          isAllTicketsActive={isAllTicketsActive}
          onStatusFilter={ticketsPage.handleStatusQuickFilter}
          onPriorityFilter={ticketsPage.handlePriorityQuickFilter}
          onResetFilter={ticketsPage.handleResetFilters}
        />
      </section>

      <section className="tablePanel">
        <TicketFilters
          filters={ticketsPage.filters}
          onChange={ticketsPage.handleFilterChange}
          onReset={ticketsPage.handleResetFilters}
        />

        <TicketTable
          tickets={ticketsPage.tickets}
          filters={ticketsPage.filters}
          total={ticketsPage.total}
          pages={ticketsPage.pages}
          isAdmin={adminAuth.isAdmin}
          updatingTicketId={ticketsPage.updatingTicketId}
          deletingTicketId={ticketsPage.deletingTicketId}
          onStatusChange={ticketsPage.handleStatusChange}
          onDelete={handleDeleteRequest}
          onEdit={handleEditTicket}
          onView={handleViewTicket}
          onPageChange={ticketsPage.handlePageChange}
          onPageSizeChange={ticketsPage.handlePageSizeChange}
        />
      </section>

      <TicketStatusPanel
        loading={ticketsPage.loading}
        error={ticketsPage.error}
        isEmpty={isTicketsEmpty}
        onErrorClose={ticketsPage.handleErrorClose}
      />

      {editingTicket && (
        <TicketEditModal
          key={editingTicket.id}
          ticket={editingTicket}
          onClose={handleEditClose}
          onUpdated={handleTicketUpdated}
        />
      )}

      {viewingTicket && (
        <TicketDetailsModal
          key={viewingTicket.id}
          ticket={viewingTicket}
          isAdmin={adminAuth.isAdmin}
          onClose={handleViewClose}
          onEdit={handleDetailsEdit}
          onDelete={handleDeleteRequest}
        />
      )}

      {deletingTicket && (
        <TicketDeleteConfirmModal
          ticket={deletingTicket}
          loading={ticketsPage.deletingTicketId === deletingTicket.id}
          onCancel={handleDeleteCancel}
          onConfirm={handleDeleteConfirm}
        />
      )}

      {isSystemInfoOpen && <SystemInfoModal onClose={handleSystemInfoClose} />}
    </main>
  );
}

export default TicketPage;
