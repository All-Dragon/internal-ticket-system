import { useState } from "react";

import styles from "../styles/AdminLoginForm.module.css";

import type { ChangeEvent, FormEvent } from "react";
import type { AdminLogin } from "../types/admin";

type AdminLoginFormProps = {
  formData: AdminLogin;
  loading: boolean;
  error: string | null;
  isAdmin: boolean;
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onLogout: () => void;
  onErrorClose: () => void;
};

function AdminLoginForm({
  formData,
  loading,
  error,
  isAdmin,
  onChange,
  onSubmit,
  onLogout,
  onErrorClose,
}: AdminLoginFormProps) {
  const [showPassword, setShowPassword] = useState<boolean>(false);

  if (isAdmin) {
    return (
      <div className={styles.root}>
        <div className={styles.state}>
          <span className={styles.stateText}>
            Вы вошли как администратор
          </span>
          <button
            className={styles.logoutButton}
            type="button"
            onClick={onLogout}
          >
            Выйти
          </button>
        </div>

        {error && (
          <p className={styles.error}>
            {error}
            <button
              className={styles.errorClose}
              type="button"
              onClick={onErrorClose}
              aria-label="Закрыть ошибку"
            >
              x
            </button>
          </p>
        )}
      </div>
    );
  }

  return (
    <div className={styles.root}>
      <form className={styles.form} onSubmit={onSubmit}>
        <label className={styles.inputGroup}>
          <span className={styles.inputIcon} aria-hidden="true">
            @
          </span>
          <input
            className={styles.field}
            type="text"
            name="username"
            value={formData.username}
            onChange={onChange}
            placeholder="Логин"
            autoComplete="username"
          />
        </label>

        <label className={styles.inputGroup}>
          <span className={styles.inputIcon} aria-hidden="true">
            #
          </span>
          <input
            className={styles.field}
            type={showPassword ? "text" : "password"}
            name="password"
            value={formData.password}
            onChange={onChange}
            placeholder="Пароль"
            autoComplete="current-password"
          />
          <button
            className={styles.passwordToggle}
            type="button"
            onClick={() => setShowPassword((prev) => !prev)}
            aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
          >
            {showPassword ? "Скрыть" : "Показать"}
          </button>
        </label>

        <button className={styles.submitButton} type="submit" disabled={loading}>
          {loading ? "Вход..." : "Войти"}
        </button>
      </form>

      {error && (
        <p className={styles.error}>
          {error}
          <button
            className={styles.errorClose}
            type="button"
            onClick={onErrorClose}
            aria-label="Закрыть ошибку"
          >
            x
          </button>
        </p>
      )}
    </div>
  );
}

export default AdminLoginForm;
