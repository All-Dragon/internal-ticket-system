import { authFetch } from "./authFetch";
import { apiUrl } from "./config";

import type { AdminLogin, TokenResponse } from "../types/admin";

export async function loginAdmin(data: AdminLogin): Promise<TokenResponse> {
    return authFetch<TokenResponse>(apiUrl("/auth/login"), {
        method: "POST",
        body: JSON.stringify(data),
    });
}
