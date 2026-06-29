const DEFAULT_ERROR_MESSAGE =
  "Произошла ошибка. Попробуйте повторить действие.";

const errorMessages: Record<string, string> = {
  "Неверные учетные данные администратора":
    "Неверный логин или пароль администратора.",
  "Требуются права администратора":
    "Для этого действия нужно войти как администратор.",
  "Заявку в статусе done нельзя редактировать или удалять":
    "Заявку в статусе Done нельзя редактировать или удалять.",
  "Нельзя перевести заявку из done обратно в другой статус":
    "Нельзя перевести заявку из Done обратно в другой статус.",
  "Заявка с таким id не найдена": "Заявка не найдена.",
  "В базе ещё нет заявок": "Заявок пока нет.",
  "Could not validate credentials": "Не удалось проверить сессию.",
  "Invalid token": "Сессия истекла. Войдите снова.",
  Unauthorized: "Сессия истекла. Войдите снова.",
  "Failed to fetch":
    "Не удалось подключиться к серверу. Проверьте соединение и попробуйте снова.",
  "Field required": "обязательное поле не заполнено.",
  "Input should be a valid string": "нужно ввести текстовое значение.",
  "String should have at least 3 characters":
    "значение должно быть не короче 3 символов.",
  "String should have at most 120 characters":
    "значение должно быть не длиннее 120 символов.",
  "String should have at most 1000 characters":
    "значение должно быть не длиннее 1000 символов.",
};

const statusMessages: Record<string, string> = {
  400: "Запрос не прошел проверку. Проверьте введенные данные.",
  401: "Сессия истекла. Войдите снова.",
  403: "У вас нет прав для этого действия.",
  404: "Запрошенные данные не найдены.",
  409: "Данные конфликтуют с текущим состоянием заявки.",
  422: "Проверьте правильность заполнения формы.",
  500: "На сервере произошла ошибка. Попробуйте позже.",
  502: "Сервер временно недоступен. Попробуйте позже.",
  503: "Сервис временно недоступен. Попробуйте позже.",
};

const fieldNames: Record<string, string> = {
  title: "заголовок",
  description: "описание",
  status: "статус",
  priority: "приоритет",
  search: "поиск",
  page: "страница",
  page_size: "количество на странице",
  username: "логин",
  password: "пароль",
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function getValidationErrorMessage(error: unknown): string | null {
  if (typeof error === "string") {
    return errorMessageHelper(error);
  }

  if (!isRecord(error)) {
    return null;
  }

  const field = Array.isArray(error.loc) ? error.loc[error.loc.length - 1] : null;
  const fieldName = typeof field === "string" ? fieldNames[field] || field : null;
  const message = errorMessageHelper(error.msg ?? error.message ?? error.type);

  if (fieldName) {
    return `Проверьте поле «${fieldName}»: ${message}`;
  }

  return message;
}

export function errorMessageHelper(error: unknown): string {
  if (!error) {
    return DEFAULT_ERROR_MESSAGE;
  }

  if (Array.isArray(error)) {
    const messages = error.map(getValidationErrorMessage).filter(Boolean);
    return messages.length ? messages.join(" ") : DEFAULT_ERROR_MESSAGE;
  }

  if (isRecord(error)) {
    if (error.detail) {
      return errorMessageHelper(error.detail);
    }

    if (error.message) {
      return errorMessageHelper(error.message);
    }

    if (error.msg) {
      return errorMessageHelper(error.msg);
    }

    return DEFAULT_ERROR_MESSAGE;
  }

  const errorText = String(error).trim();

  if (!errorText) {
    return DEFAULT_ERROR_MESSAGE;
  }

  return errorMessages[errorText] || statusMessages[errorText] || errorText;
}
