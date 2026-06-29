import { getApiErrorMessage } from '../utiles/getApiErrorMessage';

import type { ApiError } from '../types/api';

export async function authFetch<T>(
    url: string, 
    options: RequestInit = {}
): Promise<T> {
    const token = localStorage.getItem('access_token');
    const headers = new Headers(options.headers);

    headers.set("Content-Type", "application/json");

    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(url, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        const errorMessage = await getApiErrorMessage(response);
        const error = new Error(errorMessage) as ApiError;
        error.status = 401;
        throw error;
    }

    if (!response.ok) {
        const errorMessage = await getApiErrorMessage(response);
        const error = new Error(errorMessage) as ApiError;
        error.status = response.status;
        throw error;
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return response.json() as Promise<T>;
}
