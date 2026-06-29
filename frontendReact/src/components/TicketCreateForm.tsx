import useCreateTicket from "../hooks/useCreateTicket";
import styles from "../styles/TicketCreateForm.module.css";
import TicketCreatedModal from "./TicketCreatedModal";

type TicketCreateFormProps = {
  onCreated?: () => Promise<void> | void;
};

function TicketCreateForm({ onCreated }: TicketCreateFormProps) {
  const {
    formData,
    loading,
    error,
    errors,
    handleChange,
    handleSubmit,
    handleSuccessClose,
    createdTicket,
  } = useCreateTicket({ onCreated });

  return (
    <>
      <section className={styles.panel} aria-labelledby="create-ticket-title">
        <h2 className={styles.title} id="create-ticket-title">
          Создать заявку
        </h2>

        <form className={styles.form} onSubmit={handleSubmit}>
          <label className={styles.fieldGroup} htmlFor="ticket-title">
            <span className={styles.label}>
              Заголовок <span className={styles.required}>*</span>
            </span>
            <input
              className={styles.field}
              id="ticket-title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Введите заголовок (от 3 до 120 символов)"
            />
            {errors.title && <p className={styles.errorText}>{errors.title}</p>}
          </label>

          <label className={styles.fieldGroup} htmlFor="ticket-description">
            <span className={styles.label}>Описание</span>
            <textarea
              className={styles.textarea}
              id="ticket-description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Введите описание (необязательно, до 1000 символов)"
            />
            <span className={styles.textareaFooter}>
              {formData.description.length} / 1000
            </span>
            {errors.description && (
              <p className={styles.errorText}>{errors.description}</p>
            )}
          </label>

          <label className={styles.fieldGroup} htmlFor="ticket-priority">
            <span className={styles.label}>
              Приоритет <span className={styles.required}>*</span>
            </span>
            <select
              className={styles.select}
              id="ticket-priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
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

          <div className={styles.actions}>
            <button
              className={styles.submitButton}
              type="submit"
              disabled={loading}
            >
              {loading ? "Создание..." : "+ Создать заявку"}
            </button>
          </div>
        </form>
      </section>

      {createdTicket && (
        <TicketCreatedModal
          ticket={createdTicket}
          onClose={handleSuccessClose}
        />
      )}
    </>
  );
}

export default TicketCreateForm;
