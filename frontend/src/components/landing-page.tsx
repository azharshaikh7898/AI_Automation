import Link from "next/link";

const highlights = [
  "AI-assisted retention workflows",
  "Role-based workspace views",
  "Sales, customer, and order operations",
];

export function LandingPage() {
  return (
    <main className="min-h-screen px-4 py-6 md:px-6 lg:px-8">
      <div className="mx-auto grid min-h-[calc(100vh-3rem)] max-w-7xl gap-6 lg:grid-cols-[1.25fr_0.75fr]">
        <section className="glass-panel-strong relative overflow-hidden rounded-[2rem] p-8 md:p-12">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.16),transparent_32%),radial-gradient(circle_at_bottom_left,rgba(245,158,11,0.12),transparent_25%)]" />
          <div className="relative max-w-3xl">
            <p className="text-xs uppercase tracking-[0.35em] text-sky-300/80">Phase 1 Platform</p>
            <h1 className="mt-5 text-5xl font-semibold leading-tight md:text-7xl">
              Build retention and sales ops from one <span className="gradient-text">command center</span>.
            </h1>
            <p className="mt-6 max-w-2xl text-base leading-7 text-muted md:text-lg">
              Manage customers, products, orders, and follow-up workflows with a secure FastAPI backend and a focused Next.js workspace.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              {highlights.map((item) => (
                <span key={item} className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">
                  {item}
                </span>
              ))}
            </div>

            <div className="mt-10 flex flex-wrap gap-4">
              <Link href="/login" className="rounded-2xl bg-amber-400 px-6 py-3 font-semibold text-slate-950 transition hover:bg-amber-300">
                Login
              </Link>
              <Link href="/register" className="rounded-2xl border border-white/10 bg-white/5 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
                Create account
              </Link>
            </div>
          </div>
        </section>

        <aside className="glass-panel rounded-[2rem] p-8">
          <div className="flex h-full flex-col justify-between gap-8">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Phase 1 Scope</p>
              <h2 className="mt-3 text-2xl font-semibold">What is live now</h2>
            </div>

            <div className="space-y-4 text-sm text-slate-300">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                JWT auth with register, login, refresh, logout, and current-user endpoints.
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                Protected dashboard shell with sidebar navigation and role-aware session state.
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                CRUD-ready surfaces for customers, products, and orders.
              </div>
            </div>

            <p className="text-sm text-muted">
              Frontend is wired to the backend API through <span className="font-mono text-slate-100">NEXT_PUBLIC_API_BASE_URL</span>.
            </p>
          </div>
        </aside>
      </div>
    </main>
  );
}
