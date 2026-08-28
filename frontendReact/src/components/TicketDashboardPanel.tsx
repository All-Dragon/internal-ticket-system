import styles from "../styles/TicketDashboardPanel.module.css";

import type { ActiveQuickFilter } from "../hooks/useTicketsPage";
import type { Ticket, TicketPriority, TicketStatus } from "../types/ticket";

type TicketDashboardPanelProps = {
  tickets: Ticket[];
  total: number;
  activeQuickFilter: ActiveQuickFilter;
  isAllTicketsActive: boolean;
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
  isAllTicketsActive,
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
          <span
            className={`${styles.statIcon} ${styles.totalIcon}`}
            aria-hidden="true"
          >
            #
          </span>
          <div>
            <strong className={styles.statValue}>{total}</strong>
            <span className={styles.statLabel}>Найдено заявок</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span
            className={`${styles.statIcon} ${styles.newIcon}`}
            aria-hidden="true"
          >
            N
          </span>
          <div>
            <strong className={styles.statValue}>{newCount}</strong>
            <span className={styles.statLabel}>Новые на странице</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span
            className={`${styles.statIcon} ${styles.progressIcon}`}
            aria-hidden="true"
          >
            P
          </span>
          <div>
            <strong className={styles.statValue}>{inProgressCount}</strong>
            <span className={styles.statLabel}>В работе на странице</span>
          </div>
        </article>

        <article className={styles.statItem}>
          <span
            className={`${styles.statIcon} ${styles.doneIcon}`}
            aria-hidden="true"
          >
            D
          </span>
          <div>
            <strong className={styles.statValue}>{doneCount}</strong>
            <span className={styles.statLabel}>Закрыты на странице</span>
          </div>
        </article>
      </div>

      <div className={styles.actionsBlock}>
        <h3 className={styles.subtitle} id="quick-filters-title">
          Быстрые фильтры
        </h3>

        <div
          className={styles.actionsGrid}
          role="group"
          aria-labelledby="quick-filters-title"
        >
          <button
            className={getActionClassName(isAllTicketsActive)}
            type="button"
            onClick={onResetFilter}
            aria-pressed={isAllTicketsActive}
            aria-labelledby="quick-filter-all-label"
            aria-describedby="quick-filter-all-description"
          >
            <strong id="quick-filter-all-label">Все заявки</strong>
            <span id="quick-filter-all-description">Показать все заявки</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "new")}
            type="button"
            onClick={() => onStatusFilter("new")}
            aria-pressed={activeQuickFilter === "new"}
            aria-labelledby="quick-filter-new-label"
            aria-describedby="quick-filter-new-description"
          >
            <strong id="quick-filter-new-label">Новые</strong>
            <span id="quick-filter-new-description">Только New</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "in_progress")}
            type="button"
            onClick={() => onStatusFilter("in_progress")}
            aria-pressed={activeQuickFilter === "in_progress"}
            aria-labelledby="quick-filter-progress-label"
            aria-describedby="quick-filter-progress-description"
          >
            <strong id="quick-filter-progress-label">В работе</strong>
            <span id="quick-filter-progress-description">Только In Progress</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "done")}
            type="button"
            onClick={() => onStatusFilter("done")}
            aria-pressed={activeQuickFilter === "done"}
            aria-labelledby="quick-filter-done-label"
            aria-describedby="quick-filter-done-description"
          >
            <strong id="quick-filter-done-label">Закрытые</strong>
            <span id="quick-filter-done-description">Только Done</span>
          </button>

          <button
            className={getActionClassName(activeQuickFilter === "priority_high")}
            type="button"
            onClick={() => onPriorityFilter("high")}
            aria-pressed={activeQuickFilter === "priority_high"}
            aria-labelledby="quick-filter-high-label"
            aria-describedby="quick-filter-high-description"
          >
            <strong id="quick-filter-high-label">Высокий приоритет</strong>
            <span id="quick-filter-high-description">Только High</span>
          </button>
        </div>
      </div>
    </section>
  );
}

export default TicketDashboardPanel;
