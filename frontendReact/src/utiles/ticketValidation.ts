import type { TicketPriority } from "../types/ticket";

const ticketPriorities: TicketPriority[] = ["low", "normal", "high"];

export function validateTicketTitle(value: string): string | null {
  const title = value.trim();

  if (!title) {
    return "Название заявки обязательно";
  }

  if (title.length < 3) {
    return "Название должно быть не короче 3 символов";
  }

  if (title.length > 120) {
    return "Название должно быть не длиннее 120 символов";
  }

  return null;
}

export function validateTicketDescription(value: string): string | null {
  const description = value.trim();

  if (description.length > 1000) {
    return "Описание должно быть не длиннее 1000 символов";
  }

  return null;
}

export function validateTicketPriority(value: string): string | null {
  const priority = value.trim();

  if (!ticketPriorities.includes(priority as TicketPriority)) {
    return "Выберите корректный приоритет";
  }

  return null;
}
