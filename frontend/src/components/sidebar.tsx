"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

const navigationItems = [
  { href: "/dashboard", label: "Overview" },
  { href: "/dashboard/customers", label: "Customers" },
  { href: "/dashboard/products", label: "Products" },
  { href: "/dashboard/orders", label: "Orders" },
  { href: "/dashboard/triggers", label: "Triggers" },
  { href: "/dashboard/tasks", label: "Tasks" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, signOut } = useAuth();

  return (
    <aside className="glass-panel-strong flex h-full w-full flex-col gap-8 rounded-3xl p-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Customer Retention</p>
        <h2 className="mt-2 text-2xl font-semibold">Sales Command Center</h2>
      </div>

      <nav className="flex flex-1 flex-col gap-2">
        {navigationItems.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`rounded-2xl px-4 py-3 text-sm transition ${
                isActive
                  ? "bg-sky-400/15 text-white ring-1 ring-sky-300/30"
                  : "text-slate-300 hover:bg-white/5 hover:text-white"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
        <p className="font-medium text-white">{user ? `${user.first_name} ${user.last_name}` : "Account"}</p>
        <p className="mt-1 text-xs text-muted">{user?.email ?? "No active session"}</p>
        <button
          type="button"
          onClick={() => {
            void signOut();
          }}
          className="mt-4 inline-flex rounded-xl bg-amber-400 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-amber-300"
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
