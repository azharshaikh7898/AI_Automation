import Link from "next/link";
import { AuthForm } from "@/components/auth-form";

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-10">
      <section className="glass-panel-strong w-full max-w-2xl rounded-[2rem] p-8 md:p-10">
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Create Access</p>
        <h1 className="mt-3 text-3xl font-semibold">Register a new account</h1>
        <p className="mt-3 text-sm leading-6 text-muted">
          Choose a role and create the initial account for the retention and sales workspace.
        </p>

        <div className="mt-8">
          <AuthForm mode="register" />
        </div>

        <p className="mt-6 text-sm text-slate-300">
          Already registered?{" "}
          <Link href="/login" className="font-semibold text-amber-300 hover:text-amber-200">
            Sign in
          </Link>
          .
        </p>
      </section>
    </main>
  );
}
