import styles from "../styles/TicketCreatedModal.module.css";

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
  return (
    <div className={styles.backdrop}>
      <section
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="created-ticket-title"
      >
        <header className={styles.header}>
          <div>
            <h2 className={styles.title} id="created-ticket-title">
              Заявка создана
            </h2>
            <p className={styles.subtitle}>
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

        <div className={styles.content}>
          <div className={styles.row}>
            <span className={styles.label}>Статус</span>
            <p className={styles.value}>{statusLabels[ticket.status]}</p>
          </div>

          <div className={styles.row}>
            <span className={styles.label}>Приоритет</span>
            <p className={styles.value}>{priorityLabels[ticket.priority]}</p>
          </div>

          <div className={styles.row}>
            <span className={styles.label}>Описание</span>
            <p className={styles.value}>
              {ticket.description || "Не указано"}
            </p>
          </div>
        </div>

        <footer className={styles.actions}>
          <button
            className={styles.submitButton}
            type="button"
            onClick={onClose}
          >
            Понятно
          </button>
        </footer>
      </section>
    </div>
  );
}

export default TicketCreatedModal;
