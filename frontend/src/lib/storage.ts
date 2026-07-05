const AUTH_STORAGE_KEY = "customer_sales_auth";
const AUTH_COOKIE_NAME = "customer_sales_session";

export interface StoredAuth {
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
  };
  accessToken: string;
  refreshToken: string;
}

export function saveAuthSession(session: StoredAuth) {
  window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
  document.cookie = `${AUTH_COOKIE_NAME}=1; path=/; max-age=${60 * 60 * 24}; samesite=lax`;
}

export function readAuthSession(): StoredAuth | null {
  if (typeof window === "undefined") {
    return null;
  }

  const rawSession = window.localStorage.getItem(AUTH_STORAGE_KEY);
  if (!rawSession) {
    return null;
  }

  try {
    return JSON.parse(rawSession) as StoredAuth;
  } catch {
    return null;
  }
}

export function clearAuthSession() {
  window.localStorage.removeItem(AUTH_STORAGE_KEY);
  document.cookie = `${AUTH_COOKIE_NAME}=; path=/; max-age=0; samesite=lax`;
}
