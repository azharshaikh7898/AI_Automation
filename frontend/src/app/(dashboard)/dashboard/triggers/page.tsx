"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { createTrigger, deleteTrigger, fetchTriggers, updateTrigger } from "@/services/triggers";
import type { TriggerCreatePayload, TriggerRead } from "@/lib/trigger-types";

export default function TriggersPage() {
  const { accessToken, isHydrated } = useAuth();
  const [triggers, setTriggers] = useState<TriggerRead[]>([]);
  const [editingTrigger, setEditingTrigger] = useState<TriggerRead | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTriggers = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    const triggerList = await fetchTriggers(accessToken);
    setTriggers(triggerList);
  }, [accessToken]);

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    loadTriggers().catch(() => setTriggers([]));
  }, [accessToken, isHydrated, loadTriggers]);

  async function handleCreateTrigger(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const payload: TriggerCreatePayload = {
      name: String(formData.get("name") ?? "").trim(),
      trigger_type: String(formData.get("trigger_type") ?? "").trim().toLowerCase(),
      description: String(formData.get("description") ?? "").trim() || null,
      condition_expression: String(formData.get("condition_expression") ?? "").trim() || null,
      delay_minutes: Number(formData.get("delay_minutes") ?? 0),
      is_active: String(formData.get("is_active") ?? "true") === "true",
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await createTrigger(accessToken, payload);
      await loadTriggers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to create trigger");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateTrigger(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const triggerId = Number(formData.get("trigger_id") ?? 0);
    const payload: TriggerCreatePayload = {
      name: String(formData.get("name") ?? "").trim(),
      trigger_type: String(formData.get("trigger_type") ?? "").trim().toLowerCase(),
      description: String(formData.get("description") ?? "").trim() || null,
      condition_expression: String(formData.get("condition_expression") ?? "").trim() || null,
      delay_minutes: Number(formData.get("delay_minutes") ?? 0),
      is_active: String(formData.get("is_active") ?? "true") === "true",
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await updateTrigger(accessToken, triggerId, payload);
      setEditingTrigger(null);
      await loadTriggers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to update trigger");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteTrigger(triggerId: number) {
    if (!accessToken) {
      return;
    }

    if (!window.confirm("Delete this trigger?")) {
      return;
    }

    setError(null);
    try {
      await deleteTrigger(accessToken, triggerId);
      if (editingTrigger?.id === triggerId) {
        setEditingTrigger(null);
      }
      await loadTriggers();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to delete trigger");
    }
  }

  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Automation</p>
        <h1 className="mt-2 text-3xl font-semibold">Triggers</h1>
        <p className="mt-2 text-sm text-muted">Live automation rules from the FastAPI backend.</p>
      </div>

      <form action={handleCreateTrigger} className="glass-panel-strong rounded-3xl p-5">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <input name="name" placeholder="Trigger name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <select name="trigger_type" defaultValue="customer_created" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="customer_created">Customer created</option>
            <option value="order_created">Order created</option>
            <option value="payment_failed">Payment failed</option>
            <option value="invoice_overdue">Invoice overdue</option>
            <option value="inactive_customer">Inactive customer</option>
          </select>
          <input name="delay_minutes" type="number" min="0" defaultValue="0" placeholder="Delay minutes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_1fr_220px]">
          <input name="condition_expression" placeholder="Condition expression" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="description" placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <div className="flex items-end gap-3">
            <select name="is_active" defaultValue="true" className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
            <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
              {isSubmitting ? "Creating..." : "Create trigger"}
            </button>
          </div>
        </div>
        {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
      </form>

      {editingTrigger ? (
        <form action={handleUpdateTrigger} className="glass-panel-strong rounded-3xl p-5">
          <input type="hidden" name="trigger_id" value={editingTrigger.id} />
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Editing</p>
              <h2 className="mt-2 text-xl font-semibold">Update trigger</h2>
            </div>
            <button
              type="button"
              onClick={() => setEditingTrigger(null)}
              className="rounded-2xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5"
            >
              Cancel
            </button>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <input name="name" defaultValue={editingTrigger.name} placeholder="Trigger name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <select name="trigger_type" defaultValue={editingTrigger.trigger_type} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="customer_created">Customer created</option>
              <option value="order_created">Order created</option>
              <option value="payment_failed">Payment failed</option>
              <option value="invoice_overdue">Invoice overdue</option>
              <option value="inactive_customer">Inactive customer</option>
            </select>
            <input name="delay_minutes" type="number" min="0" defaultValue={editingTrigger.delay_minutes} placeholder="Delay minutes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_1fr_220px]">
            <input name="condition_expression" defaultValue={editingTrigger.condition_expression ?? ""} placeholder="Condition expression" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <input name="description" defaultValue={editingTrigger.description ?? ""} placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <div className="flex items-end gap-3">
              <select name="is_active" defaultValue={String(editingTrigger.is_active)} className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
              <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
                {isSubmitting ? "Updating..." : "Update trigger"}
              </button>
            </div>
          </div>
          {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
        </form>
      ) : null}

      <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-white/10 text-slate-300">
            <tr>
              <th className="px-5 py-4 font-medium">Name</th>
              <th className="px-5 py-4 font-medium">Type</th>
              <th className="px-5 py-4 font-medium">Delay</th>
              <th className="px-5 py-4 font-medium">Status</th>
              <th className="px-5 py-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {triggers.map((row) => (
              <tr key={row.id} className="border-b border-white/5 last:border-none">
                <td className="px-5 py-4">
                  <div>
                    <p className="font-medium text-white">{row.name}</p>
                    <p className="mt-1 text-xs text-slate-400">{row.description ?? row.condition_expression ?? "No description"}</p>
                  </div>
                </td>
                <td className="px-5 py-4 text-slate-300">{row.trigger_type}</td>
                <td className="px-5 py-4 text-slate-300">{row.delay_minutes} min</td>
                <td className="px-5 py-4 text-slate-300">{row.is_active ? "Active" : "Inactive"}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setEditingTrigger(row)}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-slate-100 transition hover:bg-white/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        void handleDeleteTrigger(row.id);
                      }}
                      className="rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-100 transition hover:bg-red-500/20"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!triggers.length ? (
              <tr>
                <td className="px-5 py-6 text-slate-400" colSpan={5}>
                  No triggers returned yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}