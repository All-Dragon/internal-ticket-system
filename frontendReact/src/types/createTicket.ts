import type { TicketPriority } from "./ticket";

export type TicketFormData = {
  title: string;
  description: string;
  priority: TicketPriority;
};

export type TicketFormErrors = Partial<Record<keyof TicketFormData, string | null>>;

export type TicketFormFieldName = keyof TicketFormData;

export const DEFAULT_TICKET_FORM_DATA: TicketFormData = {
  title: "",
  description: "",
  priority: "normal",
};