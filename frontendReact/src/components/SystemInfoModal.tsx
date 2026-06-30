import styles from "../styles/SystemInfoModal.module.css";

type SystemInfoModalProps = {
  onClose: () => void;
};

function SystemInfoModal({ onClose }: SystemInfoModalProps) {
  return (
    <div className={styles.backdrop}>
      <section
        className={styles.modal}
        role="dialog"
        aria-modal="true"
        aria-labelledby="system-info-title"
      >
        <header className={styles.header}>
          <div>
            <h2 className={styles.title} id="system-info-title">
              О системе
            </h2>
            <p className={styles.subtitle}>
              Короткие правила работы с внутренними заявками.
            </p>
          </div>

          <button
            className={styles.closeButton}
            type="button"
            onClick={onClose}
            aria-label="Закрыть информацию о системе"
          >
            x
          </button>
        </header>

        <ul className={styles.rulesList}>
          <li>Заявки в статусе Done нельзя редактировать или удалять.</li>
          <li>Нельзя перевести заявку из Done обратно в другой статус.</li>
          <li>Удаление заявки доступно только администратору.</li>
          <li>Все даты и время указаны в UTC.</li>
          <li>При нажатии на заявку откроется подробное окно просмотра заявки.</li>
          <li></li>
        </ul>
      </section>
    </div>
  );
}

export default SystemInfoModal;