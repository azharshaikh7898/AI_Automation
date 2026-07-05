import { apiFetch } from "./api";
import type { AuthResponse, LoginPayload, RegisterPayload, TokenPair } from "@/lib/types";

export function login(payload: LoginPayload) {
  return apiFetch<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function register(payload: RegisterPayload) {
  return apiFetch<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function refreshToken(refreshToken: string) {
  return apiFetch<TokenPair>("/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
}

export function logout(accessToken: string) {
  return apiFetch<void>("/auth/logout", {
    method: "POST",
    token: accessToken,
  });
}
