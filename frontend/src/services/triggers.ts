import { apiFetch } from "./api";
import type { TriggerCreatePayload, TriggerRead } from "@/lib/trigger-types";

export function fetchTriggers(token: string, offset = 0, limit = 100) {
  return apiFetch<TriggerRead[]>(`/triggers?offset=${offset}&limit=${limit}`, {
    method: "GET",
    token,
  });
}

export function createTrigger(token: string, payload: TriggerCreatePayload) {
  return apiFetch<TriggerRead>("/triggers", {
    method: "POST",
    token,
    body: JSON.stringify(payload),
  });
}

export function updateTrigger(token: string, triggerId: number, payload: Partial<TriggerCreatePayload>) {
  return apiFetch<TriggerRead>(`/triggers/${triggerId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload),
  });
}

export function deleteTrigger(token: string, triggerId: number) {
  return apiFetch<void>(`/triggers/${triggerId}`, {
    method: "DELETE",
    token,
  });
}