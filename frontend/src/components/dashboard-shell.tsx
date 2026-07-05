"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "@/components/sidebar";
import { useAuth } from "@/hooks/useAuth";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, isHydrated, user } = useAuth();

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, isHydrated, router]);

  if (!isHydrated) {
    return (
      <div className="flex min-h-screen items-center justify-center px-6 text-slate-300">
        Loading secure workspace...
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen px-4 py-4 md:px-6 lg:px-8">
      <div className="mx-auto grid min-h-[calc(100vh-2rem)] max-w-7xl gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
        <div className="sticky top-4 h-fit">
          <Sidebar />
        </div>

        <main className="glass-panel-strong rounded-3xl p-6 md:p-8">
          <div className="mb-8 flex flex-col gap-2 border-b border-white/10 pb-6 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-sky-300/80">Protected Area</p>
              <h1 className="mt-2 text-3xl font-semibold md:text-4xl">Welcome back, {user?.first_name ?? "Agent"}</h1>
            </div>
            <p className="text-sm text-muted">Role-aware dashboard shell ready for customer, product, and order operations.</p>
          </div>
          {children}
        </main>
      </div>
    </div>
  );
}
