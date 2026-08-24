import useEditTicket from "../hooks/useEditTicket";
import useModalAccessibility from "../hooks/useModalAccessibility";
import styles from "../styles/TicketEditModal.module.css";

import type { Ticket } from "../types/ticket";

type TicketEditModalProps = {
  ticket: Ticket;
  onClose: () => void;
  onUpdated?: () => Promise<void> | void;
};

function TicketEditModal({
  ticket,
  onClose,
  onUpdated,
}: TicketEditModalProps) {
  const {
    formData,
    loading,
    error,
    errors,
    success,
    handleChange,
    handleSubmit,
  } = useEditTicket({ ticket, onUpdated });

  function handleModalClose(): void {
    if (!loading) {
      onClose();
    }
  }

  const dialogRef = useModalAccessibility(handleModalClose);

  return (
    <div className={styles.backdrop}>
      <section
        ref={dialogRef}
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="edit-ticket-title"
        aria-describedby="edit-ticket-guidance"
        tabIndex={-1}
      >
        <header className={styles.header}>
          <div className={styles.heading}>
            <h2 className={styles.title} id="edit-ticket-title">
              Редактировать заявку #{ticket.id}
            </h2>
            <p className={styles.subtitle} id="edit-ticket-guidance">
              Нельзя редактировать заявку в статусе Done.
            </p>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={handleModalClose}
            disabled={loading}
            aria-label="Закрыть окно редактирования"
          >
            x
          </button>
        </header>

        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="edit-ticket-title-field">
              Заголовок
              <span className={styles.required} aria-hidden="true">
                {" "}*
              </span>
            </label>
            <input
              className={styles.field}
              id="edit-ticket-title-field"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Введите заголовок"
              disabled={loading}
              aria-required="true"
              aria-invalid={Boolean(errors.title)}
              aria-describedby={
                errors.title ? "edit-ticket-title-error" : undefined
              }
              data-modal-initial-focus
            />
            {errors.title && (
              <p
                className={styles.errorText}
                id="edit-ticket-title-error"
                role="alert"
              >
                {errors.title}
              </p>
            )}
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="edit-ticket-description">
              Описание
            </label>
            <textarea
              className={styles.textarea}
              id="edit-ticket-description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Введите описание"
              disabled={loading}
              aria-invalid={Boolean(errors.description)}
              aria-describedby={
                errors.description
                  ? "edit-ticket-description-counter edit-ticket-description-error"
                  : "edit-ticket-description-counter"
              }
            />
            <span
              className={styles.textareaFooter}
              id="edit-ticket-description-counter"
            >
              {formData.description.length} / 1000
            </span>
            {errors.description && (
              <p
                className={styles.errorText}
                id="edit-ticket-description-error"
                role="alert"
              >
                {errors.description}
              </p>
            )}
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="edit-ticket-priority">
              Приоритет
              <span className={styles.required} aria-hidden="true">
                {" "}*
              </span>
            </label>
            <select
              className={styles.select}
              id="edit-ticket-priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              disabled={loading}
              aria-required="true"
              aria-invalid={Boolean(errors.priority)}
              aria-describedby={
                errors.priority ? "edit-ticket-priority-error" : undefined
              }
            >
              <option value="low">Low</option>
              <option value="normal">Normal</option>
              <option value="high">High</option>
            </select>
            {errors.priority && (
              <p
                className={styles.errorText}
                id="edit-ticket-priority-error"
                role="alert"
              >
                {errors.priority}
              </p>
            )}
          </div>

          {error && (
            <p className={styles.errorText} role="alert">
              Ошибка: {error}
            </p>
          )}
          {success && (
            <p className={styles.successText} role="status">
              Заявка успешно обновлена.
            </p>
          )}

          <div className={styles.actions}>
            <button
              className={styles.cancelButton}
              type="button"
              onClick={handleModalClose}
              disabled={loading}
            >
              Отмена
            </button>
            <button
              className={styles.submitButton}
              type="submit"
              disabled={loading || ticket.status === "done"}
            >
              {loading ? "Сохранение..." : "Сохранить"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

export default TicketEditModal;
