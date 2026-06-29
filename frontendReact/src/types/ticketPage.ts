import type {
  SortOrder,
  TicketPriority,
  TicketSortBy,
  TicketStatus,
} from "./ticket";

export type TicketFilters = {
  status: "" | TicketStatus;
  priority: "" | TicketPriority;
  search: string;
  sort_by: TicketSortBy;
  sort_order: SortOrder;
  page: number;
  page_size: number;
};

export const DEFAULT_FILTERS: TicketFilters = {
  status: "",
  priority: "",
  search: "",
  sort_by: "created_at",
  sort_order: "desc",
  page: 1,
  page_size: 10,
};
