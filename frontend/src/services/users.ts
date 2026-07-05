import { apiFetch } from "./api";
import type { AuthenticatedUser } from "@/lib/types";

export function fetchCurrentUser(token: string) {
  return apiFetch<AuthenticatedUser>("/users/me", {
    method: "GET",
    token,
  });
}
