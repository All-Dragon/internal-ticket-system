export type TicketStatus = "new" | "in_progress" | "done";
export type TicketPriority = "low" | "normal" | "high";
export type TicketSortBy = "created_at" | "priority" | "status";
export type SortOrder = "asc" | "desc";

export type Ticket = {
  id: number;
  title: string;
  description: string | null;
  status: TicketStatus;
  priority: TicketPriority;
  created_at: string;
  updated_at: string;
};

export type TicketCreate = {
  title: string;
  description?: string | null;
  priority: TicketPriority;
};

export type TicketUpdate = {
  title: string;
  description?: string | null;
  priority: TicketPriority;
};

export type TicketStatusUpdate = {
  status: TicketStatus;
};

export type TicketListParams = {
  status?: TicketStatus;
  priority?: TicketPriority;
  search?: string;
  sort_by?: TicketSortBy;
  sort_order?: SortOrder;
  page?: number;
  page_size?: number;
};

export type TicketListResponse = {
  items: Ticket[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
};
