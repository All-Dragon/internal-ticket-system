import { useState } from "react";

import AdminLoginForm from "./components/AdminLoginForm";
import TicketCreateForm from "./components/TicketCreateForm";
import TicketEditModal from "./components/TicketEditModal";
import TicketFilters from "./components/TicketFilters";
import TicketStatusPanel from "./components/TicketStatusPanel";
import TicketTable from "./components/TicketTable";

import useAdminAuth from "./hooks/useAdminAuth";
import useTicketsPage from "./hooks/useTicketsPage";

import type { Ticket } from "./types/ticket";

import "./App.css";

function App() {
  const adminAuth = useAdminAuth();
  const ticketsPage = useTicketsPage();

  async function handleTicketCreated(): Promise<void> {
    await ticketsPage.loadTickets({
      ...ticketsPage.filters,
      page: 1,
    });
  }

  const [editingTicket, setEditingTicket] = useState<Ticket | null>(null);

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

  const isTicketsEmpty = !ticketsPage.loading && ticketsPage.tickets.length === 0;

  return (
    <main className="appPage">
      <header className="appHeader">
        <h1 className="appTitle">Внутренние заявки</h1>

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

        <section className="systemPanel" aria-labelledby="system-title">
          <h2 id="system-title">О системе</h2>

          <ul className="rulesList">
            <li>Заявки в статусе Done нельзя редактировать или удалять.</li>
            <li>Нельзя перевести заявку из Done обратно в другой статус.</li>
            <li>Удаление заявки доступно только администратору.</li>
            <li>Все даты и время указаны в UTC.</li>
          </ul>
        </section>
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
          onDelete={ticketsPage.handleDeleteTicket}
          onEdit={handleEditTicket}
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
    </main>
  );
}

export default App;
