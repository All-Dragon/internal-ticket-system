import styles from "../styles/TicketStatusPanel.module.css";

type TicketStatusPanelProps = {
  loading: boolean;
  error: string;
  isEmpty: boolean;
  onErrorClose?: () => void;
};

function TicketStatusPanel({
  loading,
  error,
  isEmpty,
  onErrorClose,
}: TicketStatusPanelProps) {
  if (!loading && !error && !isEmpty) {
    return null;
  }

  return (
    <div className={styles.root}>
      {loading && (
        <section className={`${styles.panel} ${styles.loadingPanel}`}>
          <span className={styles.icon} aria-hidden="true">
            ...
          </span>
          <div className={styles.content}>
            <h2 className={styles.title}>Загрузка...</h2>
            <p className={styles.text}>Пожалуйста, подождите.</p>
          </div>
        </section>
      )}

      {!loading && isEmpty && (
        <section className={`${styles.panel} ${styles.emptyPanel}`}>
          <span className={styles.icon} aria-hidden="true">
            -
          </span>
          <div className={styles.content}>
            <h2 className={styles.title}>Заявки не найдены</h2>
            <p className={styles.text}>
              Попробуйте изменить параметры поиска.
            </p>
          </div>
        </section>
      )}

      {error && (
        <section className={`${styles.panel} ${styles.errorPanel}`}>
          <span className={styles.icon} aria-hidden="true">
            !
          </span>
          <div className={styles.content}>
            <h2 className={styles.title}>Ошибка</h2>
            <p className={styles.text}>{error}</p>
          </div>

          {onErrorClose && (
            <button
              className={styles.closeButton}
              type="button"
              onClick={onErrorClose}
              aria-label="Закрыть ошибку"
            >
              x
            </button>
          )}
        </section>
      )}
    </div>
  );
}

export default TicketStatusPanel;
