import styles from "../styles/TicketDashboardPanel.module.css";

import type { ActiveQuickFilter } from "../hooks/useTicketsPage";
import type { Ticket, TicketPriority, TicketStatus } from "../types/ticket";

type TicketDashboardPanelProps = {
  tickets: Ticket[];
  total: number;
  activeQuickFilter: ActiveQuickFilter;
  onStatusFilter: (status: "" | TicketStatus) => void;
  onPriorityFilter: (priority: "" | TicketPriority) => void;
  onResetFilter: () => void;
};

function getActionClassName(isActive: boolean): string {
  return isActive
    ? `${styles.actionButton} ${styles.activeActionButton}`
    : styles.actionButton;
}

function TicketDashboardPanel({
  tickets,
  total,
  activeQuickFilter,
  onStatusFilter,
  onPriorityFilter,
  onResetFilter,
}: TicketDashboardPanelProps) {
  const newCount = tickets.filter((ticket) => ticket.status === "new").length;
  const inProgressCount = tickets.filter(
    (ticket) => ticket.status === "in_progress",
  ).length;
  const doneCount = tickets.filter((ticket) => ticket.status === "done").length;

  return (
    <section className={styles.panel} aria-labelledby="dashboard-title">
      <h2 className={styles.title} id="dashboard-title">
        Быстрая статистика
      </h2>

      <div className={styles.statsGrid}>
        <article className={styles.statItem}>
          <span className={`${styles.statIcon} ${styles.totalIcon}`}>#</span>
          <div>
            <strong className={styles.statValue}>{total}</strong>
            <span className={styles.statLabel}>Найдено заявок</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span className={`${styles.statIcon} ${styles.newIcon}`}>N</span>
          <div>
            <strong className={styles.statValue}>{newCount}</strong>
            <span className={styles.statLabel}>Новые на странице</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span className={`${styles.statIcon} ${styles.progressIcon}`}>P</span>
          <div>
            <strong className={styles.statValue}>{inProgressCount}</strong>
            <span className={styles.statLabel}>В работе на странице</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span className={`${styles.statIcon} ${styles.doneIcon}`}>D</span>
          <div>
            <strong className={styles.statValue}>{doneCount}</strong>
            <span className={styles.statLabel}>Закрыты на странице</span>
          </div>
        </article>
      </div>

      <div className={styles.actionsBlock}>
        <h3 className={styles.subtitle}>Быстрые фильтры</h3>

        <div className={styles.actionsGrid}>
          <button
            className={styles.actionButton}
            type="button"
            onClick={onResetFilter}
            aria-pressed={false}
          >
            <strong>Все заявки</strong>
            <span>Показать все заявки</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "new")}
            type="button"
            onClick={() => onStatusFilter("new")}
            aria-pressed={activeQuickFilter === "new"}
          >
            <strong>Новые</strong>
            <span>Только New</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "in_progress")}
            type="button"
            onClick={() => onStatusFilter("in_progress")}
            aria-pressed={activeQuickFilter === "in_progress"}
          >
            <strong>В работе</strong>
            <span>Только In Progress</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "done")}
            type="button"
            onClick={() => onStatusFilter("done")}
            aria-pressed={activeQuickFilter === "done"}
          >
            <strong>Закрытые</strong>
            <span>Только Done</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "priority_high")}
            type="button"
            onClick={() => onPriorityFilter("high")}
            aria-pressed={activeQuickFilter === "priority_high"}
          >
            <strong>Высокий приоритет</strong>
            <span>Только High</span>
          </button>
        </div>
      </div>
    </section>
  );
}

export default TicketDashboardPanel;
