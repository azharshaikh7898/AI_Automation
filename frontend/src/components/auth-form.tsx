"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import type { LoginPayload, RegisterPayload, RoleName } from "@/lib/types";

interface AuthFormProps {
  mode: "login" | "register";
}

const roleOptions: RoleName[] = ["Sales Executive", "Manager", "Admin"];

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const { signIn, signUp } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);

    try {
      if (mode === "login") {
        const payload: LoginPayload = {
          email: String(formData.get("email") ?? "").trim(),
          password: String(formData.get("password") ?? ""),
        };
        await signIn(payload);
        router.push("/dashboard");
      } else {
        const payload: RegisterPayload = {
          first_name: String(formData.get("first_name") ?? "").trim(),
          last_name: String(formData.get("last_name") ?? "").trim(),
          email: String(formData.get("email") ?? "").trim(),
          phone_number: String(formData.get("phone_number") ?? "").trim() || null,
          password: String(formData.get("password") ?? ""),
          role_name: String(formData.get("role_name") ?? "Sales Executive") as RoleName,
        };
        await signUp(payload);
        router.push("/dashboard");
      }
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Something went wrong");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      {mode === "register" ? (
        <div className="grid gap-4 md:grid-cols-2">
          <input
            name="first_name"
            placeholder="First name"
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-sky-300/50"
            required
          />
          <input
            name="last_name"
            placeholder="Last name"
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-sky-300/50"
            required
          />
        </div>
      ) : null}

      <input
        type="email"
        name="email"
        placeholder="Email address"
        className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-sky-300/50"
        required
      />

      {mode === "register" ? (
        <input
          name="phone_number"
          placeholder="Phone number"
          className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-sky-300/50"
        />
      ) : null}

      {mode === "register" ? (
        <select
          name="role_name"
          defaultValue="Sales Executive"
          className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none focus:border-sky-300/50"
        >
          {roleOptions.map((role) => (
            <option key={role} value={role}>
              {role}
            </option>
          ))}
        </select>
      ) : null}

      <input
        type="password"
        name="password"
        placeholder="Password"
        className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-sky-300/50"
        required
      />

      {error ? <p className="rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-flex w-full items-center justify-center rounded-2xl bg-amber-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-amber-300 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Processing..." : mode === "login" ? "Sign in" : "Create account"}
      </button>
    </form>
  );
}
