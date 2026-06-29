import styles from "../styles/TicketTable.module.css";

import type { ChangeEvent } from "react";
import type { Ticket, TicketPriority, TicketStatus } from "../types/ticket";
import type { TicketFilters } from "../types/ticketPage";

type TicketTableProps = {
  tickets: Ticket[];
  filters: TicketFilters;
  total: number;
  pages: number;
  isAdmin: boolean;
  updatingTicketId: number | null;
  deletingTicketId: number | null;
  onStatusChange: (id: number, status: TicketStatus) => void;
  onDelete: (id: number) => void;
  onEdit: (ticket: Ticket) => void;
  onView: (ticket: Ticket) => void;
  onPageChange: (page: number) => void;
  onPageSizeChange: (event: ChangeEvent<HTMLSelectElement>) => void;
};

const statusLabels: Record<TicketStatus, string> = {
  new: "New",
  in_progress: "In Progress",
  done: "Done",
};

const priorityLabels: Record<TicketPriority, string> = {
  low: "Low",
  normal: "Normal",
  high: "High",
};

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  }).format(new Date(value));
}

function getStatusClassName(status: TicketStatus): string {
  switch (status) {
    case "new":
      return `${styles.statusSelect} ${styles.statusNew}`;

    case "in_progress":
      return `${styles.statusSelect} ${styles.statusProgress}`;

    case "done":
      return `${styles.statusSelect} ${styles.statusDone}`;

    default:
      return styles.statusSelect;
  }
}

function getPriorityClassName(priority: TicketPriority): string {
  switch (priority) {
    case "low":
      return `${styles.prioritySelect} ${styles.priorityLow}`;

    case "normal":
      return `${styles.prioritySelect} ${styles.priorityNormal}`;

    case "high":
      return `${styles.prioritySelect} ${styles.priorityHigh}`;

    default:
      return styles.prioritySelect;
  }
}

function getPageNumbers(currentPage: number, pages: number): number[] {
  return Array.from({ length: pages }, (_, index) => index + 1).filter(
    (page) => {
      if (pages <= 5) {
        return true;
      }

      return page === 1 || page === pages || Math.abs(page - currentPage) <= 1;
    },
  );
}

function TicketTable({
  tickets,
  filters,
  total,
  pages,
  isAdmin,
  updatingTicketId,
  deletingTicketId,
  onStatusChange,
  onDelete,
  onEdit,
  onView,
  onPageChange,
  onPageSizeChange,
}: TicketTableProps) {
  if (!tickets.length) {
    return null;
  }

  const firstItemNumber = (filters.page - 1) * filters.page_size + 1;
  const lastItemNumber = Math.min(filters.page * filters.page_size, total);
  const pageNumbers = getPageNumbers(filters.page, pages);

  return (
    <section className={styles.panel} aria-label="Список заявок">
      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <colgroup>
            <col className={styles.idColumn} />
            <col className={styles.titleColumn} />
            <col className={styles.descriptionColumn} />
            <col className={styles.statusColumn} />
            <col className={styles.priorityColumn} />
            <col className={styles.dateColumn} />
            <col className={styles.dateColumn} />
            <col className={styles.actionsColumn} />
          </colgroup>

          <thead>
            <tr>
              <th>ID</th>
              <th>Заголовок</th>
              <th>Описание</th>
              <th>Статус</th>
              <th>Приоритет</th>
              <th>Создано (UTC)</th>
              <th>Обновлено (UTC)</th>
              <th>Действия</th>
            </tr>
          </thead>

          <tbody>
            {tickets.map((ticket) => {
              const isDone = ticket.status === "done";
              const isUpdating = updatingTicketId === ticket.id;
              const isDeleting = deletingTicketId === ticket.id;
              const canDelete = isAdmin && !isDone;
              const canEdit = !isDone;

              return (
                <tr
                  key={ticket.id}
                  className={styles.row}
                  onClick={() => onView(ticket)}
                >
                  <td className={styles.idCell}>#{ticket.id}</td>

                  <td className={styles.titleCell}>{ticket.title}</td>

                  <td className={styles.descriptionCell}>
                    <span
                      className={styles.descriptionText}
                      title={ticket.description || "Без описания"}
                    >
                      {ticket.description || (
                        <span className={styles.mutedText}>Без описания</span>
                      )}
                    </span>
                  </td>

                  <td>
                    <select
                      className={getStatusClassName(ticket.status)}
                      value={ticket.status}
                      disabled={isDone || isUpdating}
                      onClick={(event) => event.stopPropagation()}
                      onChange={(event) =>
                        onStatusChange(
                          ticket.id,
                          event.target.value as TicketStatus,
                        )
                      }
                    >
                      {Object.entries(statusLabels).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </td>

                  <td>
                    <span className={getPriorityClassName(ticket.priority)}>
                      {priorityLabels[ticket.priority]}
                    </span>
                  </td>

                  <td>{formatDate(ticket.created_at)}</td>
                  <td>{formatDate(ticket.updated_at)}</td>

                  <td>
                    <div className={styles.actions}>
                      <button
                        className={`${styles.actionButton} ${styles.viewButton}`}
                        type="button"
                        onClick={(event) => {
                          event.stopPropagation();
                          onView(ticket);
                        }}
                        title="Посмотреть заявку"
                      >
                        Смотр.
                      </button>

                      <button
                        className={`${styles.actionButton} ${styles.editButton}`}
                        type="button"
                        disabled={!canEdit}
                        onClick={(event) => {
                          event.stopPropagation();
                          onEdit(ticket);
                        }}
                        title={
                          isDone
                            ? "Заявку в статусе Done нельзя редактировать"
                            : "Редактировать заявку"
                        }
                      >
                        Ред.
                      </button>

                      {isAdmin ? (
                        <button
                          className={`${styles.actionButton} ${styles.dangerButton}`}
                          type="button"
                          disabled={!canDelete || isDeleting}
                          onClick={(event) => {
                            event.stopPropagation();
                            onDelete(ticket.id);
                          }}
                          title={
                            isDone
                              ? "Заявку в статусе Done нельзя удалить"
                              : "Удалить заявку"
                          }
                        >
                          {isDeleting ? "..." : "Удалить"}
                        </button>
                      ) : null}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <footer className={styles.footer}>
        <span className={styles.summary}>
          Показано {firstItemNumber}-{lastItemNumber} из {total} заявок
        </span>

        <div className={styles.pagination} aria-label="Пагинация">
          <button
            className={styles.pageButton}
            type="button"
            disabled={filters.page <= 1}
            onClick={() => onPageChange(filters.page - 1)}
          >
            Назад
          </button>

          {pageNumbers.map((page) => (
            <button
              key={page}
              className={
                page === filters.page
                  ? `${styles.pageButton} ${styles.activePage}`
                  : styles.pageButton
              }
              type="button"
              onClick={() => onPageChange(page)}
            >
              {page}
            </button>
          ))}

          <button
            className={styles.pageButton}
            type="button"
            disabled={filters.page >= pages}
            onClick={() => onPageChange(filters.page + 1)}
          >
            Далее
          </button>
        </div>

        <label className={styles.pageSize}>
          На странице:
          <select
            className={styles.pageSizeSelect}
            name="page_size"
            value={filters.page_size}
            onChange={onPageSizeChange}
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
          </select>
        </label>
      </footer>
    </section>
  );
}

export default TicketTable;
