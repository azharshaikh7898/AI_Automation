"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { createCustomer, deleteCustomer, fetchCustomers, updateCustomer } from "@/services/customers";
import type { CustomerCreatePayload, CustomerRead } from "@/lib/types";

export default function CustomersPage() {
  const { accessToken, isHydrated } = useAuth();
  const [customers, setCustomers] = useState<CustomerRead[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<CustomerRead | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadCustomers = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    const customerList = await fetchCustomers(accessToken);
    setCustomers(customerList);
  }, [accessToken]);

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    loadCustomers().catch(() => setCustomers([]));
  }, [accessToken, isHydrated, loadCustomers]);

  async function handleCreateCustomer(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const payload: CustomerCreatePayload = {
      first_name: String(formData.get("first_name") ?? "").trim(),
      last_name: String(formData.get("last_name") ?? "").trim(),
      email: String(formData.get("email") ?? "").trim() || null,
      phone_number: String(formData.get("phone_number") ?? "").trim() || null,
      company_name: String(formData.get("company_name") ?? "").trim() || null,
      status: String(formData.get("status") ?? "lead").trim().toLowerCase(),
      source: String(formData.get("source") ?? "").trim() || null,
      notes: String(formData.get("notes") ?? "").trim() || null,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await createCustomer(accessToken, payload);
      await loadCustomers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to create customer");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateCustomer(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const customerId = Number(formData.get("customer_id") ?? 0);
    const payload: CustomerCreatePayload = {
      first_name: String(formData.get("first_name") ?? "").trim(),
      last_name: String(formData.get("last_name") ?? "").trim(),
      email: String(formData.get("email") ?? "").trim() || null,
      phone_number: String(formData.get("phone_number") ?? "").trim() || null,
      company_name: String(formData.get("company_name") ?? "").trim() || null,
      status: String(formData.get("status") ?? "lead").trim().toLowerCase(),
      source: String(formData.get("source") ?? "").trim() || null,
      notes: String(formData.get("notes") ?? "").trim() || null,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await updateCustomer(accessToken, customerId, payload);
      setEditingCustomer(null);
      await loadCustomers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to update customer");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteCustomer(customerId: number) {
    if (!accessToken) {
      return;
    }

    if (!window.confirm("Delete this customer?")) {
      return;
    }

    setError(null);
    try {
      await deleteCustomer(accessToken, customerId);
      if (editingCustomer?.id === customerId) {
        setEditingCustomer(null);
      }
      await loadCustomers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to delete customer");
    }
  }

  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Workspace</p>
        <h1 className="mt-2 text-3xl font-semibold">Customers</h1>
        <p className="mt-2 text-sm text-muted">Live customer list from the FastAPI backend.</p>
      </div>

      <form
        action={handleCreateCustomer}
        className="glass-panel-strong rounded-3xl p-5"
      >
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <input name="first_name" placeholder="First name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <input name="last_name" placeholder="Last name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <input name="email" type="email" placeholder="Email" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="phone_number" placeholder="Phone number" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="company_name" placeholder="Company name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="source" placeholder="Source" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[180px_1fr]">
          <select name="status" defaultValue="lead" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="lead">Lead</option>
            <option value="prospect">Prospect</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="churned">Churned</option>
          </select>
          <input name="notes" placeholder="Notes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
        <button type="submit" disabled={isSubmitting} className="mt-4 rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
          {isSubmitting ? "Creating..." : "Create customer"}
        </button>
      </form>

      {editingCustomer ? (
        <form action={handleUpdateCustomer} className="glass-panel-strong rounded-3xl p-5">
          <input type="hidden" name="customer_id" value={editingCustomer.id} />
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Editing</p>
              <h2 className="mt-2 text-xl font-semibold">Update customer</h2>
            </div>
            <button
              type="button"
              onClick={() => setEditingCustomer(null)}
              className="rounded-2xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5"
            >
              Cancel
            </button>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <input name="first_name" defaultValue={editingCustomer.first_name} placeholder="First name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <input name="last_name" defaultValue={editingCustomer.last_name} placeholder="Last name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <input name="email" type="email" defaultValue={editingCustomer.email ?? ""} placeholder="Email" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <input name="phone_number" defaultValue={editingCustomer.phone_number ?? ""} placeholder="Phone number" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <input name="company_name" defaultValue={editingCustomer.company_name ?? ""} placeholder="Company name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <input name="source" defaultValue={editingCustomer.source ?? ""} placeholder="Source" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[180px_1fr]">
            <select name="status" defaultValue={editingCustomer.status} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="lead">Lead</option>
              <option value="prospect">Prospect</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="churned">Churned</option>
            </select>
            <input name="notes" defaultValue={editingCustomer.notes ?? ""} placeholder="Notes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          </div>
          {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
          <button type="submit" disabled={isSubmitting} className="mt-4 rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
            {isSubmitting ? "Updating..." : "Update customer"}
          </button>
        </form>
      ) : null}

      <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-white/10 text-slate-300">
            <tr>
              <th className="px-5 py-4 font-medium">Name</th>
              <th className="px-5 py-4 font-medium">Status</th>
              <th className="px-5 py-4 font-medium">Company</th>
              <th className="px-5 py-4 font-medium">Email</th>
              <th className="px-5 py-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((row) => (
              <tr key={row.id} className="border-b border-white/5 last:border-none">
                <td className="px-5 py-4">{row.first_name} {row.last_name}</td>
                <td className="px-5 py-4 text-slate-300">{row.status}</td>
                <td className="px-5 py-4 text-slate-300">{row.company_name ?? "-"}</td>
                <td className="px-5 py-4 text-slate-300">{row.email ?? "-"}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setEditingCustomer(row)}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-slate-100 transition hover:bg-white/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        void handleDeleteCustomer(row.id);
                      }}
                      className="rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-100 transition hover:bg-red-500/20"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!customers.length ? (
              <tr>
                <td className="px-5 py-6 text-slate-400" colSpan={5}>
                  No customers returned yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}
