import { useState } from "react";

import { loginAdmin } from "../api/auth";

import type { ChangeEvent, FormEvent } from "react";
import type { AdminLogin } from "../types/admin";

const DEFAULT_ADMIN_FORM_DATA: AdminLogin = {
  username: "",
  password: "",
};

function useAdminAuth() {
  const [formData, setFormData] = useState<AdminLogin>(
    DEFAULT_ADMIN_FORM_DATA,
  );
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState<boolean>(
    Boolean(localStorage.getItem("access_token")),
  );

  function handleChange(event: ChangeEvent<HTMLInputElement>): void {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setError(null);
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Введите логин и пароль администратора");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const token = await loginAdmin({
        username: formData.username.trim(),
        password: formData.password,
      });

      localStorage.setItem("access_token", token.access_token);
      setIsAdmin(true);
      setFormData(DEFAULT_ADMIN_FORM_DATA);
    } catch (submitError) {
      localStorage.removeItem("access_token");
      setIsAdmin(false);

      const message =
        submitError instanceof Error
          ? submitError.message
          : "Не удалось войти как администратор";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleLogout(): void {
    localStorage.removeItem("access_token");
    setIsAdmin(false);
    setError(null);
    setFormData(DEFAULT_ADMIN_FORM_DATA);
  }

  function handleErrorClose(): void {
    setError(null);
  }

  return {
    formData,
    loading,
    error,
    isAdmin,
    handleChange,
    handleSubmit,
    handleLogout,
    handleErrorClose,
  };
}

export default useAdminAuth;
