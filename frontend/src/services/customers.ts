import { apiFetch } from "./api";
import type { CustomerCreatePayload, CustomerRead } from "@/lib/types";

export function fetchCustomers(token: string, offset = 0, limit = 100) {
  return apiFetch<CustomerRead[]>(`/customers?offset=${offset}&limit=${limit}`, {
    method: "GET",
    token,
  });
}

export function createCustomer(token: string, payload: CustomerCreatePayload) {
  return apiFetch<CustomerRead>("/customers", {
    method: "POST",
    token,
    body: JSON.stringify(payload),
  });
}

export function updateCustomer(token: string, customerId: number, payload: Partial<CustomerCreatePayload>) {
  return apiFetch<CustomerRead>(`/customers/${customerId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload),
  });
}

export function deleteCustomer(token: string, customerId: number) {
  return apiFetch<void>(`/customers/${customerId}`, {
    method: "DELETE",
    token,
  });
}
