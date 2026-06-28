import { authFetch, publicFetch } from "./authFetch";
import { apiUrl } from "./config";

export async function createUser(data) {
  return publicFetch("/users", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function loginUser(data) {
  return publicFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getUserProfile() {
  return authFetch(apiUrl("/users/me"), {
    method: "GET",
  });
}
