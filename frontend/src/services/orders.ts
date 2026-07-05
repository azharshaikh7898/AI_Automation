import { apiFetch } from "./api";
import type { OrderCreatePayload, OrderRead } from "@/lib/types";

export function fetchOrders(token: string, offset = 0, limit = 100) {
  return apiFetch<OrderRead[]>(`/orders?offset=${offset}&limit=${limit}`, {
    method: "GET",
    token,
  });
}

export function createOrder(token: string, payload: OrderCreatePayload) {
  return apiFetch<OrderRead>("/orders", {
    method: "POST",
    token,
    body: JSON.stringify(payload),
  });
}

export function updateOrder(token: string, orderId: number, payload: Partial<OrderCreatePayload>) {
  return apiFetch<OrderRead>(`/orders/${orderId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload),
  });
}

export function deleteOrder(token: string, orderId: number) {
  return apiFetch<void>(`/orders/${orderId}`, {
    method: "DELETE",
    token,
  });
}
