const DEFAULT_ERROR_MESSAGE = "Произошла ошибка. Попробуйте повторить действие.";

const errorMessages: Record<string, string> = {
    // Auth
    "Неверный пароль": "Введен неверный пароль. Проверьте пароль и попробуйте еще раз.",
    "Пароль не совпадает": "Текущий пароль введен неверно.",
    "Пользователь не найден": "Пользователь с такими данными не найден. Проверьте email или зарегистрируйтесь.",
    "Пользователь деактивирован": "Аккаунт деактивирован. Обратитесь к администратору.",
    "Ошибка генерации токена": "Не удалось выполнить вход. Попробуйте еще раз позже.",
    Unauthorized: "Сессия истекла. Войдите снова.",
    "Invalid token": "Сессия истекла. Войдите снова.",
    "Could not validate credentials": "Не удалось проверить сессию. Войдите снова.",
    "User not found": "Пользователь из текущей сессии не найден. Войдите снова.",
    "User is inactive": "Аккаунт деактивирован. Обратитесь к администратору.",

    // Users
    "В базе ещё нет пользователей": "Список пользователей пока пуст.",
    "Пользователь с таким id не найден": "Пользователь не найден.",
    "Пользователь с таким email не найден": "Пользователь с таким email не найден. Проверьте введенный email.",
    "Пользователя с таким email нет в базе": "Пользователь с таким email не найден. Проверьте введенный email.",
    "В базе ещё нет пользователей без места учебы": "Пользователей без места учебы пока нет.",
    "Пользователь уже существует!": "Пользователь с таким email уже зарегистрирован. Войдите или используйте другой email.",
    "Вы не можете создать Админский аккаунт!": "Нельзя создать админский аккаунт через эту форму.",
    "Такого университета нет в базе, проверьте правильность написания названия.":
        "Мы не нашли такой университет. Проверьте название или оставьте поле пустым.",
    "В базе нет университета с таким id": "Университет не найден. Выберите другой университет.",
    "Ошибка soft delete пользователя": "Не удалось удалить профиль. Попробуйте позже.",
    "Ошибка hard delete пользователя": "Не удалось окончательно удалить пользователя. Попробуйте позже.",

    // Universities
    "В базе нет университетов": "Список университетов пока пуст.",
    "Университет с таким названием не найден": "Университет с таким названием не найден.",
    "Университет с таким id не найден": "Университет не найден.",
    "В базе нет университетов из этого города": "В выбранном городе университеты не найдены.",
    "Такой университет уже есть в базе": "Такой университет уже добавлен.",
    "В базе нет университета с таким названием": "Университет с таким названием не найден.",
    "Нет университета с таким названием": "Университет с таким названием не найден.",
    "Ошибка hard delete университета": "Не удалось окончательно удалить университет. Попробуйте позже.",

    // Units
    "В базе нет units!": "Список единиц измерения пока пуст.",
    "Unit под этим id не найден!": "Единица измерения не найдена.",
    "Unit под этим именем не найден!": "Единица измерения с таким названием не найдена.",
    "В базе нет unit с symbol": "Единица измерения с таким символом не найдена.",
    "Unit с таким названием уже существует!": "Единица измерения с таким названием уже существует.",
    "В базе нет unit с таким названием": "Единица измерения с таким названием не найдена.",
    "Нет unit с таким названием": "Единица измерения с таким названием не найдена.",
    "Ошибка hard delete unit": "Не удалось окончательно удалить единицу измерения. Попробуйте позже.",

    // Exercises
    "В базе нет упражнений": "Список упражнений пока пуст.",
    "В базе нет такого упражнения": "Упражнение не найдено.",
    "В базе нет упражнений из этой категории": "В выбранной категории упражнений пока нет.",
    "Такое упражнение уже есть!": "Такое упражнение уже добавлено.",
    "Ошибка при удалении упражнения": "Не удалось удалить упражнение. Попробуйте позже.",

    // Norms
    "No norms found in database.": "Список нормативов пока пуст.",
    "Norm with this id was not found.": "Норматив не найден.",
    "Exercise with this id was not found.": "Упражнение не найдено.",
    "Exercise with this name was not found.": "Упражнение с таким названием не найдено.",
    "No norms found for this exercise.": "Для выбранного упражнения нормативы не найдены.",
    "No norms found for this step.": "Для выбранной ступени ГТО нормативы не найдены.",
    "No norms found for this gender.": "Для выбранного пола нормативы не найдены.",
    "Norm with these parameters was not found.": "Норматив с такими параметрами не найден.",
    "Could not determine GTO step for this user.": "Не удалось определить ступень ГТО для пользователя.",
    "No norms found for this user.": "Для этого пользователя нормативы не найдены.",
    "Unit with this id was not found.": "Единица измерения не найдена.",
    "Unit with this name was not found.": "Единица измерения с таким названием не найдена.",
    "A norm with these parameters already exists.": "Норматив с такими параметрами уже существует.",

    // FastAPI validation
    "Field required": "обязательное поле не заполнено.",
    "Input should be a valid string": "нужно ввести текстовое значение.",
    "Input should be a valid integer": "нужно ввести целое число.",
    "Input should be a valid number": "нужно ввести число.",
    "Input should be a valid date": "нужно выбрать корректную дату.",
    "Input should be a valid email address": "нужно ввести корректный email.",
    "String should have at least 1 character": "поле не должно быть пустым.",

    // Common
    "Ошибка сервера": "На сервере произошла ошибка. Попробуйте позже.",
    "Server error.": "На сервере произошла ошибка. Попробуйте позже.",
    "Failed to fetch": "Не удалось подключиться к серверу. Проверьте соединение и попробуйте снова.",
};

const statusMessages: Record<string, string> = {
    400: "Запрос не прошел проверку. Проверьте введенные данные.",
    401: "Сессия истекла. Войдите снова.",
    403: "У вас нет прав для этого действия.",
    404: "Запрошенные данные не найдены.",
    409: "Эти данные конфликтуют с уже существующими.",
    422: "Проверьте правильность заполнения формы.",
    500: "На сервере произошла ошибка. Попробуйте позже.",
    502: "Сервер временно недоступен. Попробуйте позже.",
    503: "Сервис временно недоступен. Попробуйте позже.",
};

const fieldNames: Record<string, string> = {
    birth_date: "дата рождения",
    email: "email",
    faculty: "факультет",
    full_name: "ФИО",
    gender: "пол",
    group_name: "группа",
    password: "пароль",
    role: "роль",
    university: "университет",
};

function getDynamicErrorMessage(error: string): string | null {
    if (error.startsWith("Access denied. Required roles:")) {
        return "У вас нет прав для этого действия.";
    }

    return null;
}

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

    return (
        errorMessages[errorText] ||
        statusMessages[errorText] ||
        getDynamicErrorMessage(errorText) ||
        errorText
    );
}
