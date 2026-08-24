import styles from "../styles/TicketDetailsModal.module.css";
import useModalAccessibility from "../hooks/useModalAccessibility";

import type { Ticket } from "../types/ticket";

type TicketDetailsModalProps = {
  ticket: Ticket;
  isAdmin: boolean;
  onClose: () => void;
  onEdit: (ticket: Ticket) => void;
  onDelete: (ticket: Ticket) => void;
};

const statusLabels: Record<Ticket["status"], string> = {
  new: "New",
  in_progress: "In Progress",
  done: "Done",
};

const priorityLabels: Record<Ticket["priority"], string> = {
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

function getStatusClassName(status: Ticket["status"]): string {
  switch (status) {
    case "new":
      return `${styles.badge} ${styles.statusNew}`;

    case "in_progress":
      return `${styles.badge} ${styles.statusProgress}`;

    case "done":
      return `${styles.badge} ${styles.statusDone}`;

    default:
      return styles.badge;
  }
}

function getPriorityClassName(priority: Ticket["priority"]): string {
  switch (priority) {
    case "low":
      return `${styles.badge} ${styles.priorityLow}`;

    case "normal":
      return `${styles.badge} ${styles.priorityNormal}`;

    case "high":
      return `${styles.badge} ${styles.priorityHigh}`;

    default:
      return styles.badge;
  }
}

function TicketDetailsModal({
  ticket,
  isAdmin,
  onClose,
  onEdit,
  onDelete,
}: TicketDetailsModalProps) {
  const isDone = ticket.status === "done";
  const description = ticket.description || "Описание не указано";
  const dialogRef = useModalAccessibility(onClose);

  return (
    <div className={styles.backdrop}>
      <section
        ref={dialogRef}
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="ticket-details-title"
        tabIndex={-1}
      >
        <header className={styles.header}>
          <div className={styles.heading}>
            <h2 className={styles.title} id="ticket-details-title">
              Подробности заявки
            </h2>

            <div className={styles.titleRow}>
              <span className={styles.ticketId}>#{ticket.id}</span>
              <strong className={styles.ticketTitle}>{ticket.title}</strong>
            </div>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={onClose}
            aria-label="Закрыть подробности заявки"
            data-modal-initial-focus
          >
            x
          </button>
        </header>

        <div className={styles.content}>
          <dl className={styles.summary}>
            <div className={styles.summaryItem}>
              <dt className={styles.summaryLabel}>Статус</dt>
              <dd className={getStatusClassName(ticket.status)}>
                {statusLabels[ticket.status]}
              </dd>
            </div>

            <div className={styles.summaryItem}>
              <dt className={styles.summaryLabel}>Приоритет</dt>
              <dd className={getPriorityClassName(ticket.priority)}>
                {priorityLabels[ticket.priority]}
              </dd>
            </div>

            <div className={styles.summaryItem}>
              <dt className={styles.summaryLabel}>Создано (UTC)</dt>
              <dd className={styles.summaryValue}>
                {formatDate(ticket.created_at)}
              </dd>
            </div>

            <div className={styles.summaryItem}>
              <dt className={styles.summaryLabel}>Обновлено (UTC)</dt>
              <dd className={styles.summaryValue}>
                {formatDate(ticket.updated_at)}
              </dd>
            </div>
          </dl>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Описание</h3>
            <p className={styles.description}>{description}</p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>
              Дополнительная информация
            </h3>

            <dl className={styles.metaList}>
              <div className={styles.metaItem}>
                <dt>ID</dt>
                <dd>{ticket.id}</dd>
              </div>

              <div className={styles.metaItem}>
                <dt>Время создания</dt>
                <dd>{formatDate(ticket.created_at)} (UTC)</dd>
              </div>

              <div className={styles.metaItem}>
                <dt>Время обновления</dt>
                <dd>{formatDate(ticket.updated_at)} (UTC)</dd>
              </div>
            </dl>
          </section>
        </div>

        <footer className={styles.actions}>
          {isDone ? (
            <p className={styles.actionHint}>
              Завершённые заявки недоступны для редактирования и удаления.
            </p>
          ) : null}

          <div className={styles.actionButtons}>
            <button
              className={styles.editButton}
              type="button"
              disabled={isDone}
              onClick={() => onEdit(ticket)}
              title={
                isDone
                  ? "Заявку в статусе Done нельзя редактировать"
                  : "Редактировать заявку"
              }
            >
              Редактировать
            </button>

            {isAdmin && (
              <button
                className={styles.deleteButton}
                type="button"
                disabled={isDone}
                onClick={() => onDelete(ticket)}
                title={
                  isDone
                    ? "Заявку в статусе Done нельзя удалить"
                    : "Удалить заявку"
                }
              >
                Удалить заявку
              </button>
            )}
          </div>
        </footer>
      </section>
    </div>
  );
}

export default TicketDetailsModal;
