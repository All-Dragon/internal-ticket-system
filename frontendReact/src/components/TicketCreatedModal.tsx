import styles from "../styles/TicketCreatedModal.module.css";
import useModalAccessibility from "../hooks/useModalAccessibility";

import type { Ticket } from "../types/ticket";

type TicketCreatedModalProps = {
  ticket: Ticket;
  onClose: () => void;
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

function TicketCreatedModal({ ticket, onClose }: TicketCreatedModalProps) {
  const dialogRef = useModalAccessibility(onClose);

  return (
    <div className={styles.backdrop}>
      <section
        ref={dialogRef}
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="created-ticket-title"
        aria-describedby="created-ticket-summary"
        tabIndex={-1}
      >
        <header className={styles.header}>
          <div>
            <h2 className={styles.title} id="created-ticket-title">
              Заявка создана
            </h2>
            <p className={styles.subtitle} id="created-ticket-summary">
              #{ticket.id} {ticket.title}
            </p>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={onClose}
            aria-label="Закрыть информацию о созданной заявке"
          >
            x
          </button>
        </header>

        <dl className={styles.content}>
          <div className={styles.row}>
            <dt className={styles.label}>Статус</dt>
            <dd className={styles.value}>{statusLabels[ticket.status]}</dd>
          </div>

          <div className={styles.row}>
            <dt className={styles.label}>Приоритет</dt>
            <dd className={styles.value}>{priorityLabels[ticket.priority]}</dd>
          </div>

          <div className={styles.row}>
            <dt className={styles.label}>Описание</dt>
            <dd className={styles.value}>
              {ticket.description || "Не указано"}
            </dd>
          </div>
        </dl>

        <footer className={styles.actions}>
          <button
            className={styles.submitButton}
            type="button"
            onClick={onClose}
            data-modal-initial-focus
          >
            Понятно
          </button>
        </footer>
      </section>
    </div>
  );
}

export default TicketCreatedModal;
