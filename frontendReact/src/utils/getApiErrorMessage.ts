import { errorMessageHelper } from "./errorMessageHelper";

export async function getApiErrorMessage(response: Response): Promise<string> {
    try {
        const data = await response.json();

        if (data.detail) {
            return errorMessageHelper(data.detail);
        }

        if (data.message) {
            return errorMessageHelper(data.message);
        }
    } catch {
        return errorMessageHelper(response.status);
    }

    return errorMessageHelper(response.status);
}