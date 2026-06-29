import styles from "../styles/TicketFilters.module.css";

import type { ChangeEvent } from "react";
import type { TicketFilters } from "../types/ticketPage";

type TicketFiltersProps = {
  filters: TicketFilters;
  onChange: (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  onReset: () => void;
};

function TicketFilters({ filters, onChange, onReset }: TicketFiltersProps) {
  return (
    <div className={styles.root}>
      <label className={styles.fieldGroup} htmlFor="ticket-search">
        <span className={styles.label}>Поиск</span>
        <span className={styles.searchWrap}>
          <span className={styles.searchIcon} aria-hidden="true">
            ?
          </span>
          <input
            className={styles.field}
            id="ticket-search"
            name="search"
            type="search"
            value={filters.search}
            onChange={onChange}
            placeholder="Поиск по заголовку или описанию..."
          />
        </span>
      </label>

      <label className={styles.fieldGroup} htmlFor="ticket-status-filter">
        <span className={styles.label}>Статус</span>
        <select
          className={styles.select}
          id="ticket-status-filter"
          name="status"
          value={filters.status}
          onChange={onChange}
        >
          <option value="">Все статусы</option>
          <option value="new">New</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </label>

      <label className={styles.fieldGroup} htmlFor="ticket-priority-filter">
        <span className={styles.label}>Приоритет</span>
        <select
          className={styles.select}
          id="ticket-priority-filter"
          name="priority"
          value={filters.priority}
          onChange={onChange}
        >
          <option value="">Все приоритеты</option>
          <option value="low">Low</option>
          <option value="normal">Normal</option>
          <option value="high">High</option>
        </select>
      </label>

      <label className={styles.fieldGroup} htmlFor="ticket-sort-by">
        <span className={styles.label}>Сортировать по</span>
        <select
          className={styles.select}
          id="ticket-sort-by"
          name="sort_by"
          value={filters.sort_by}
          onChange={onChange}
        >
          <option value="created_at">Дата создания</option>
          <option value="priority">Приоритет</option>
          <option value="status">Статус</option>
        </select>
      </label>

      <label className={styles.fieldGroup} htmlFor="ticket-sort-order">
        <span className={styles.label}>Порядок</span>
        <select
          className={styles.select}
          id="ticket-sort-order"
          name="sort_order"
          value={filters.sort_order}
          onChange={onChange}
        >
          <option value="desc">По убыванию</option>
          <option value="asc">По возрастанию</option>
        </select>
      </label>

      <button className={styles.resetButton} type="button" onClick={onReset}>
        Сбросить
      </button>
    </div>
  );
}

export default TicketFilters;