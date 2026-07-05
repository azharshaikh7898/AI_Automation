import { apiFetch } from "./api";
import type { TaskCreatePayload, TaskRead } from "@/lib/task-types";

export function fetchTasks(token: string, offset = 0, limit = 100) {
  return apiFetch<TaskRead[]>(`/tasks?offset=${offset}&limit=${limit}`, {
    method: "GET",
    token,
  });
}

export function createTask(token: string, payload: TaskCreatePayload) {
  return apiFetch<TaskRead>("/tasks", {
    method: "POST",
    token,
    body: JSON.stringify(payload),
  });
}

export function updateTask(token: string, taskId: number, payload: Partial<TaskCreatePayload>) {
  return apiFetch<TaskRead>(`/tasks/${taskId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload),
  });
}

export function deleteTask(token: string, taskId: number) {
  return apiFetch<void>(`/tasks/${taskId}`, {
    method: "DELETE",
    token,
  });
}