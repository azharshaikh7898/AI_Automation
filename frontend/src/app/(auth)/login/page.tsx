import Link from "next/link";
import { AuthForm } from "@/components/auth-form";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-10">
      <section className="glass-panel-strong w-full max-w-md rounded-[2rem] p-8 md:p-10">
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Secure Access</p>
        <h1 className="mt-3 text-3xl font-semibold">Sign in to your workspace</h1>
        <p className="mt-3 text-sm leading-6 text-muted">
          Use your company account to access customers, products, and sales automation tools.
        </p>

        <div className="mt-8">
          <AuthForm mode="login" />
        </div>

        <p className="mt-6 text-sm text-slate-300">
          No account yet?{" "}
          <Link href="/register" className="font-semibold text-amber-300 hover:text-amber-200">
            Create one here
          </Link>
          .
        </p>
      </section>
    </main>
  );
}
