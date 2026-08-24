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
          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="ticket-title">
              Заголовок
              <span className={styles.required} aria-hidden="true">
                {" "}*
              </span>
            </label>
            <input
              className={styles.field}
              id="ticket-title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Введите заголовок (от 3 до 120 символов)"
              aria-required="true"
              aria-invalid={Boolean(errors.title)}
              aria-describedby={errors.title ? "ticket-title-error" : undefined}
            />
            {errors.title && (
              <p
                className={styles.errorText}
                id="ticket-title-error"
                role="alert"
              >
                {errors.title}
              </p>
            )}
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="ticket-description">
              Описание
            </label>
            <textarea
              className={styles.textarea}
              id="ticket-description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Введите описание (необязательно, до 1000 символов)"
              aria-invalid={Boolean(errors.description)}
              aria-describedby={
                errors.description
                  ? "ticket-description-counter ticket-description-error"
                  : "ticket-description-counter"
              }
            />
            <span
              className={styles.textareaFooter}
              id="ticket-description-counter"
            >
              {formData.description.length} / 1000
            </span>
            {errors.description && (
              <p
                className={styles.errorText}
                id="ticket-description-error"
                role="alert"
              >
                {errors.description}
              </p>
            )}
          </div>

          <div className={styles.fieldGroup}>
            <label className={styles.label} htmlFor="ticket-priority">
              Приоритет
              <span className={styles.required} aria-hidden="true">
                {" "}*
              </span>
            </label>
            <select
              className={styles.select}
              id="ticket-priority"
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              aria-required="true"
              aria-invalid={Boolean(errors.priority)}
              aria-describedby={
                errors.priority ? "ticket-priority-error" : undefined
              }
            >
              <option value="low">Low</option>
              <option value="normal">Normal</option>
              <option value="high">High</option>
            </select>
            {errors.priority && (
              <p
                className={styles.errorText}
                id="ticket-priority-error"
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
