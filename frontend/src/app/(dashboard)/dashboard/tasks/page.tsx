"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { fetchCurrentUser } from "@/services/users";
import { fetchCustomers } from "@/services/customers";
import { fetchTriggers } from "@/services/triggers";
import { createTask, deleteTask, fetchTasks, updateTask } from "@/services/tasks";
import type { AuthenticatedUser, CustomerRead } from "@/lib/types";
import type { TaskCreatePayload, TaskRead } from "@/lib/task-types";
import type { TriggerRead } from "@/lib/trigger-types";

export default function TasksPage() {
  const { accessToken, isHydrated } = useAuth();
  const [tasks, setTasks] = useState<TaskRead[]>([]);
  const [customers, setCustomers] = useState<CustomerRead[]>([]);
  const [triggers, setTriggers] = useState<TriggerRead[]>([]);
  const [currentUser, setCurrentUser] = useState<AuthenticatedUser | null>(null);
  const [editingTask, setEditingTask] = useState<TaskRead | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    const [taskList, customerList, triggerList, user] = await Promise.all([
      fetchTasks(accessToken),
      fetchCustomers(accessToken),
      fetchTriggers(accessToken),
      fetchCurrentUser(accessToken),
    ]);

    setTasks(taskList);
    setCustomers(customerList);
    setTriggers(triggerList);
    setCurrentUser(user);
  }, [accessToken]);

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    loadTasks().catch(() => {
      setTasks([]);
      setCustomers([]);
      setTriggers([]);
      setCurrentUser(null);
    });
  }, [accessToken, isHydrated, loadTasks]);

  async function handleCreateTask(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const assignedUserRaw = String(formData.get("assigned_user_id") ?? "").trim();
    const payload: TaskCreatePayload = {
      customer_id: Number(formData.get("customer_id") ?? 0),
      assigned_user_id: assignedUserRaw ? Number(assignedUserRaw) : null,
      trigger_id: Number(formData.get("trigger_id") ?? 0) || null,
      title: String(formData.get("title") ?? "").trim(),
      description: String(formData.get("description") ?? "").trim() || null,
      status: String(formData.get("status") ?? "pending").trim().toLowerCase(),
      priority: String(formData.get("priority") ?? "medium").trim().toLowerCase(),
      due_date: String(formData.get("due_date") ?? "").trim() || null,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await createTask(accessToken, payload);
      await loadTasks();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to create task");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateTask(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const taskId = Number(formData.get("task_id") ?? 0);
    const assignedUserRaw = String(formData.get("assigned_user_id") ?? "").trim();
    const payload: TaskCreatePayload = {
      customer_id: Number(formData.get("customer_id") ?? 0),
      assigned_user_id: assignedUserRaw ? Number(assignedUserRaw) : null,
      trigger_id: Number(formData.get("trigger_id") ?? 0) || null,
      title: String(formData.get("title") ?? "").trim(),
      description: String(formData.get("description") ?? "").trim() || null,
      status: String(formData.get("status") ?? "pending").trim().toLowerCase(),
      priority: String(formData.get("priority") ?? "medium").trim().toLowerCase(),
      due_date: String(formData.get("due_date") ?? "").trim() || null,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await updateTask(accessToken, taskId, payload);
      setEditingTask(null);
      await loadTasks();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to update task");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteTask(taskId: number) {
    if (!accessToken) {
      return;
    }

    if (!window.confirm("Delete this task?")) {
      return;
    }

    setError(null);
    try {
      await deleteTask(accessToken, taskId);
      if (editingTask?.id === taskId) {
        setEditingTask(null);
      }
      await loadTasks();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to delete task");
    }
  }

  const customerLookup = new Map(customers.map((customer) => [customer.id, `${customer.first_name} ${customer.last_name}`]));
  const triggerLookup = new Map(triggers.map((trigger) => [trigger.id, trigger.name]));

  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Workflow</p>
        <h1 className="mt-2 text-3xl font-semibold">Tasks</h1>
        <p className="mt-2 text-sm text-muted">Live follow-up tasks from the FastAPI backend.</p>
      </div>

      <form action={handleCreateTask} className="glass-panel-strong rounded-3xl p-5">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <select name="customer_id" defaultValue="" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none" required>
            <option value="" disabled>Select customer</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.first_name} {customer.last_name}
              </option>
            ))}
          </select>
          <select name="trigger_id" defaultValue="" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="">No trigger</option>
            {triggers.map((trigger) => (
              <option key={trigger.id} value={trigger.id}>
                {trigger.name}
              </option>
            ))}
          </select>
          <input
            name="assigned_user_id"
            type="number"
            min="1"
            defaultValue={currentUser?.id ?? ""}
            placeholder="Assigned user id"
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none"
          />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_180px_180px]">
          <input name="title" placeholder="Task title" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <select name="status" defaultValue="pending" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="pending">Pending</option>
            <option value="in_progress">In progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <select name="priority" defaultValue="medium" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_220px]">
          <input name="description" placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="due_date" type="datetime-local" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        <div className="mt-4 flex justify-end">
          <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
            {isSubmitting ? "Creating..." : "Create task"}
          </button>
        </div>
        {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
      </form>

      {editingTask ? (
        <form action={handleUpdateTask} className="glass-panel-strong rounded-3xl p-5">
          <input type="hidden" name="task_id" value={editingTask.id} />
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Editing</p>
              <h2 className="mt-2 text-xl font-semibold">Update task</h2>
            </div>
            <button type="button" onClick={() => setEditingTask(null)} className="rounded-2xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5">
              Cancel
            </button>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <select name="customer_id" defaultValue={editingTask.customer_id} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none" required>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.first_name} {customer.last_name}
                </option>
              ))}
            </select>
            <select name="trigger_id" defaultValue={editingTask.trigger_id ?? ""} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="">No trigger</option>
              {triggers.map((trigger) => (
                <option key={trigger.id} value={trigger.id}>
                  {trigger.name}
                </option>
              ))}
            </select>
            <input
              name="assigned_user_id"
              type="number"
              min="1"
              defaultValue={editingTask.assigned_user_id ?? ""}
              placeholder="Assigned user id"
              className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none"
            />
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_180px_180px]">
            <input name="title" defaultValue={editingTask.title} placeholder="Task title" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <select name="status" defaultValue={editingTask.status} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="pending">Pending</option>
              <option value="in_progress">In progress</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <select name="priority" defaultValue={editingTask.priority} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_220px]">
            <input name="description" defaultValue={editingTask.description ?? ""} placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <input
              name="due_date"
              type="datetime-local"
              defaultValue={editingTask.due_date ? editingTask.due_date.slice(0, 16) : ""}
              className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none"
            />
          </div>
          <div className="mt-4 flex justify-end">
            <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
              {isSubmitting ? "Updating..." : "Update task"}
            </button>
          </div>
          {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
        </form>
      ) : null}

      <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-white/10 text-slate-300">
            <tr>
              <th className="px-5 py-4 font-medium">Title</th>
              <th className="px-5 py-4 font-medium">Customer</th>
              <th className="px-5 py-4 font-medium">Trigger</th>
              <th className="px-5 py-4 font-medium">Status</th>
              <th className="px-5 py-4 font-medium">Priority</th>
              <th className="px-5 py-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((row) => (
              <tr key={row.id} className="border-b border-white/5 last:border-none">
                <td className="px-5 py-4">
                  <div>
                    <p className="font-medium text-white">{row.title}</p>
                    <p className="mt-1 text-xs text-slate-400">{row.description ?? "No description"}</p>
                  </div>
                </td>
                <td className="px-5 py-4 text-slate-300">{customerLookup.get(row.customer_id) ?? `Customer #${row.customer_id}`}</td>
                <td className="px-5 py-4 text-slate-300">{row.trigger_id ? triggerLookup.get(row.trigger_id) ?? `Trigger #${row.trigger_id}` : "-"}</td>
                <td className="px-5 py-4 text-slate-300">{row.status}</td>
                <td className="px-5 py-4 text-slate-300">{row.priority}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setEditingTask(row)}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-slate-100 transition hover:bg-white/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        void handleDeleteTask(row.id);
                      }}
                      className="rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-100 transition hover:bg-red-500/20"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!tasks.length ? (
              <tr>
                <td className="px-5 py-6 text-slate-400" colSpan={6}>
                  No tasks returned yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}