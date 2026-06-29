import { useState } from "react";

import { createTicket } from "../api/ticket";
import {
  validateTicketDescription,
  validateTicketPriority,
  validateTicketTitle,
} from "../utiles/ticketValidation";
import { DEFAULT_TICKET_FORM_DATA } from "../types/createTicket";

import type { ChangeEvent, FormEvent } from "react";
import type { Ticket, TicketCreate } from "../types/ticket";
import type {
  TicketFormData,
  TicketFormErrors,
  TicketFormFieldName,
} from "../types/createTicket";

type UseCreateTicketParams = {
  onCreated?: () => Promise<void> | void;
};

function useCreateTicket({ onCreated }: UseCreateTicketParams = {}) {
  const [formData, setFormData] = useState<TicketFormData>(
    DEFAULT_TICKET_FORM_DATA,
  );
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<TicketFormErrors>({});
  const [success, setSuccess] = useState<boolean>(false);
  const [createdTicket, setCreatedTicket] = useState<Ticket | null>(null);

  function validateField(
    name: TicketFormFieldName,
    value: string,
  ): string | null {
    switch (name) {
      case "title":
        return validateTicketTitle(value);

      case "description":
        return validateTicketDescription(value);

      case "priority":
        return validateTicketPriority(value);

      default:
        return null;
    }
  }

  function validateForm(): TicketFormErrors {
    return {
      title: validateTicketTitle(formData.title),
      description: validateTicketDescription(formData.description),
      priority: validateTicketPriority(formData.priority),
    };
  }

  function handleChange(
    event: ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ): void {
    const { value, name } = event.target;
    const fieldName = name as TicketFormFieldName;

    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));

    setErrors((prev) => ({
      ...prev,
      [fieldName]: validateField(fieldName, value),
    }));
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const validationErrors = validateForm();
    const hasErrors = Object.values(validationErrors).some(
      (item) => item !== null,
    );

    if (hasErrors) {
      setErrors(validationErrors);
      return;
    }

    const payload: TicketCreate = {
      title: formData.title.trim(),
      description: formData.description.trim() || null,
      priority: formData.priority,
    };

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      const ticket = await createTicket(payload);

      setCreatedTicket(ticket);
      setSuccess(true);
      setFormData(DEFAULT_TICKET_FORM_DATA);
      setErrors({});

      await onCreated?.();
    } catch (submitError) {
      const message =
        submitError instanceof Error
          ? submitError.message
          : "Не удалось создать заявку";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleSuccessClose(): void {
    setSuccess(false);
    setCreatedTicket(null);
  }

  return {
    formData,
    loading,
    error,
    errors,
    success,
    createdTicket,
    handleChange,
    handleSubmit,
    handleSuccessClose,
  };
}

export default useCreateTicket;
