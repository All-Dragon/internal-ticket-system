import styles from "../styles/TicketDeleteConfirmModal.module.css";
import useModalAccessibility from "../hooks/useModalAccessibility";

import type { Ticket } from "../types/ticket";

type TicketDeleteConfirmModalProps = {
  ticket: Ticket;
  loading: boolean;
  onCancel: () => void;
  onConfirm: (id: number) => void;
};

function TicketDeleteConfirmModal({
  ticket,
  loading,
  onCancel,
  onConfirm,
}: TicketDeleteConfirmModalProps) {
  function handleModalClose(): void {
    if (!loading) {
      onCancel();
    }
  }

  const dialogRef = useModalAccessibility(handleModalClose);

  return (
    <div className={styles.backdrop}>
      <section
        ref={dialogRef}
        className={styles.modal}
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="delete-ticket-title"
        aria-describedby="delete-ticket-warning"
        tabIndex={-1}
      >
        <header className={styles.header}>
          <div>
            <h2 className={styles.title} id="delete-ticket-title">
              Удалить заявку?
            </h2>
            <p className={styles.subtitle}>
              #{ticket.id} {ticket.title}
            </p>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={handleModalClose}
            disabled={loading}
            aria-label="Закрыть подтверждение удаления"
          >
            x
          </button>
        </header>

        <div className={styles.content}>
          <p className={styles.text} id="delete-ticket-warning">
            Это действие нельзя отменить. Заявка будет удалена из системы.
          </p>
        </div>

        <footer className={styles.actions}>
          <button
            className={styles.cancelButton}
            type="button"
            onClick={handleModalClose}
            disabled={loading}
            data-modal-initial-focus
          >
            Отмена
          </button>

          <button
            className={styles.deleteButton}
            type="button"
            onClick={() => onConfirm(ticket.id)}
            disabled={loading}
          >
            {loading ? "Удаление..." : "Удалить заявку"}
          </button>
        </footer>
      </section>
    </div>
  );
}

export default TicketDeleteConfirmModal;
