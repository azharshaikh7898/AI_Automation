"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { AuthResponse, AuthenticatedUser, LoginPayload, RegisterPayload } from "@/lib/types";
import { clearAuthSession, readAuthSession, saveAuthSession, type StoredAuth } from "@/lib/storage";
import { fetchCurrentUser } from "@/services/users";
import { login as loginRequest, register as registerRequest, logout as logoutRequest } from "@/services/auth";

function createStoredSession(response: AuthResponse): StoredAuth {
  return {
    user: {
      id: response.user.id,
      first_name: response.user.first_name,
      last_name: response.user.last_name,
      email: response.user.email,
    },
    accessToken: response.tokens.access_token,
    refreshToken: response.tokens.refresh_token,
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

export function useAuth() {
  const router = useRouter();
  const [storedSession, setStoredSession] = useState<StoredAuth | null>(null);
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    const session = readAuthSession();
    setStoredSession(session);
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!storedSession) {
      setUser(null);
      return;
    }

    fetchCurrentUser(storedSession.accessToken)
      .then((currentUser) => setUser(currentUser))
      .catch(() => {
        clearAuthSession();
        setStoredSession(null);
        setUser(null);
      });
  }, [storedSession]);

  async function persistAuth(response: AuthResponse) {
    const session = createStoredSession(response);
    saveAuthSession(session);
    setStoredSession(session);
    setUser(response.user);
    router.push("/dashboard");
  }

  async function signIn(payload: LoginPayload) {
    const response = await loginRequest(payload);
    await persistAuth(response);
  }

  async function signUp(payload: RegisterPayload) {
    const response = await registerRequest(payload);
    await persistAuth(response);
  }

  async function signOut() {
    if (storedSession) {
      await logoutRequest(storedSession.accessToken).catch(() => undefined);
    }

    clearAuthSession();
    setStoredSession(null);
    setUser(null);
    router.push("/login");
  }

  async function refreshUser() {
    if (!storedSession) {
      return;
    }

    const currentUser = await fetchCurrentUser(storedSession.accessToken);
    setUser(currentUser);
  }

  return {
    user,
    accessToken: storedSession?.accessToken ?? null,
    isHydrated,
    isAuthenticated: Boolean(storedSession),
    signIn,
    signUp,
    signOut,
    refreshUser,
  };
}
