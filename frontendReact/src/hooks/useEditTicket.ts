import { useState } from "react";

import { updateTicket } from "../api/ticket";
import {
  validateTicketDescription,
  validateTicketPriority,
  validateTicketTitle,
} from "../utiles/ticketValidation";

import type { ChangeEvent, FormEvent } from "react";
import type { Ticket, TicketUpdate } from "../types/ticket";
import type {
  TicketFormData,
  TicketFormErrors,
  TicketFormFieldName,
} from "../types/createTicket";

type UseEditTicketParams = {
  ticket: Ticket | null;
  onUpdated?: () => Promise<void> | void;
};

function getInitialFormData(ticket: Ticket | null): TicketFormData {
  if (!ticket) {
    return {
      title: "",
      description: "",
      priority: "normal",
    };
  }

  return {
    title: ticket.title,
    description: ticket.description ?? "",
    priority: ticket.priority,
  };
}

function useEditTicket({ ticket, onUpdated }: UseEditTicketParams) {
  const [formData, setFormData] = useState<TicketFormData>(() =>
    getInitialFormData(ticket),
  );
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<TicketFormErrors>({});
  const [success, setSuccess] = useState<boolean>(false);

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

    setError(null);
    setSuccess(false);
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (!ticket) {
      setError("Заявка не выбрана");
      return;
    }

    const validationErrors = validateForm();
    const hasErrors = Object.values(validationErrors).some(
      (item) => item !== null,
    );

    if (hasErrors) {
      setErrors(validationErrors);
      return;
    }

    const payload: TicketUpdate = {
      title: formData.title.trim(),
      description: formData.description.trim() || null,
      priority: formData.priority,
    };

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      await updateTicket(ticket.id, payload);

      setSuccess(true);
      setErrors({});

      await onUpdated?.();
    } catch (submitError) {
      const message =
        submitError instanceof Error
          ? submitError.message
          : "Не удалось обновить заявку";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleSuccessClose(): void {
    setSuccess(false);
  }

  function handleErrorClose(): void {
    setError(null);
  }

  return {
    formData,
    loading,
    error,
    errors,
    success,
    handleChange,
    handleSubmit,
    handleSuccessClose,
    handleErrorClose,
  };
}

export default useEditTicket;
