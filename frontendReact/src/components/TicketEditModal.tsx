import useEditTicket from "../hooks/useEditTicket";
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

  return (
    <div className={styles.backdrop}>
      <section
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="edit-ticket-title"
      >
        <header className={styles.header}>
          <div className={styles.heading}>
            <h2 className={styles.title} id="edit-ticket-title">
              Редактировать заявку #{ticket.id}
            </h2>
            <p className={styles.subtitle}>
              Нельзя редактировать заявку в статусе Done.
            </p>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={onClose}
            disabled={loading}
            aria-label="Закрыть окно редактирования"
          >
            x
          </button>
        </header>

        <form className={styles.form} onSubmit={handleSubmit}>
          <label className={styles.fieldGroup} htmlFor="edit-ticket-title-field">
            <span className={styles.label}>
              Заголовок <span className={styles.required}>*</span>
            </span>
            <input
              className={styles.field}
              id="edit-ticket-title-field"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Введите заголовок"
              disabled={loading}
            />
            {errors.title && <p className={styles.errorText}>{errors.title}</p>}
          </label>

          <label
            className={styles.fieldGroup}
            htmlFor="edit-ticket-description"
          >
            <span className={styles.label}>Описание</span>
            <textarea
              className={styles.textarea}
              id="edit-ticket-description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Введите описание"
              disabled={loading}
            />
            <span className={styles.textareaFooter}>
              {formData.description.length} / 1000
            </span>
            {errors.description && (
              <p className={styles.errorText}>{errors.description}</p>
            )}
          </label>

          <label className={styles.fieldGroup} htmlFor="edit-ticket-priority">
            <span className={styles.label}>
              Приоритет <span className={styles.required}>*</span>
            </span>
            <select
              className={styles.select}
              id="edit-ticket-priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              disabled={loading}
            >
              <option value="low">Low</option>
              <option value="normal">Normal</option>
              <option value="high">High</option>
            </select>
            {errors.priority && (
              <p className={styles.errorText}>{errors.priority}</p>
            )}
          </label>

          {error && <p className={styles.errorText}>Ошибка: {error}</p>}
          {success && (
            <p className={styles.successText}>Заявка успешно обновлена.</p>
          )}

          <div className={styles.actions}>
            <button
              className={styles.cancelButton}
              type="button"
              onClick={onClose}
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