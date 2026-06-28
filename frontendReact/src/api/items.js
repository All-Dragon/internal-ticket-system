import { authFetch } from "./authFetch";
import { apiUrl } from "./config";

export async function getMyItems() {
  return authFetch(apiUrl("/items/my"), {
    method: "GET",
  });
}

export async function createItem(data) {
  return authFetch(apiUrl("/items"), {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateItem(id, data) {
  return authFetch(apiUrl(`/items/${id}`), {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteItem(id) {
  return authFetch(apiUrl(`/items/${id}`), {
    method: "DELETE",
  });
}
