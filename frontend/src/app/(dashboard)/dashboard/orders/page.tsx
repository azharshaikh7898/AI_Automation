"use client";

import { useCallback, useEffect, useState } from "react";
import { createOrder, deleteOrder, fetchOrders, updateOrder } from "@/services/orders";
import { fetchCustomers } from "@/services/customers";
import { fetchProducts } from "@/services/products";
import { useAuth } from "@/hooks/useAuth";
import type { CustomerRead, OrderCreatePayload, OrderRead, ProductRead } from "@/lib/types";

export default function OrdersPage() {
  const { accessToken, isHydrated } = useAuth();
  const [orders, setOrders] = useState<OrderRead[]>([]);
  const [customers, setCustomers] = useState<CustomerRead[]>([]);
  const [products, setProducts] = useState<ProductRead[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingOrder, setEditingOrder] = useState<OrderRead | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadOrders = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    const [orderList, customerList, productList] = await Promise.all([
      fetchOrders(accessToken),
      fetchCustomers(accessToken),
      fetchProducts(accessToken),
    ]);

    setOrders(orderList);
    setCustomers(customerList);
    setProducts(productList);
  }, [accessToken]);

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    loadOrders().catch(() => {
      setOrders([]);
      setCustomers([]);
      setProducts([]);
    });
  }, [accessToken, isHydrated, loadOrders]);

  async function handleCreateOrder(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const payload: OrderCreatePayload = {
      customer_id: Number(formData.get("customer_id") ?? 0),
      order_number: String(formData.get("order_number") ?? "").trim(),
      status: String(formData.get("status") ?? "draft").trim().toLowerCase(),
      currency: String(formData.get("currency") ?? "USD").trim().toUpperCase(),
      notes: String(formData.get("notes") ?? "").trim() || null,
      items: [
        {
          product_id: Number(formData.get("product_id") ?? 0),
          quantity: Number(formData.get("quantity") ?? 1),
          unit_price: String(formData.get("unit_price") ?? "0.00").trim(),
        },
      ],
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await createOrder(accessToken, payload);
      await loadOrders();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to create order");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateOrder(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const orderId = Number(formData.get("order_id") ?? 0);
    const payload = {
      customer_id: Number(formData.get("customer_id") ?? 0),
      status: String(formData.get("status") ?? "draft").trim().toLowerCase(),
      currency: String(formData.get("currency") ?? "USD").trim().toUpperCase(),
      notes: String(formData.get("notes") ?? "").trim() || null,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await updateOrder(accessToken, orderId, payload);
      setEditingOrder(null);
      await loadOrders();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to update order");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteOrder(orderId: number) {
    if (!accessToken) {
      return;
    }

    if (!window.confirm("Delete this order?")) {
      return;
    }

    setError(null);
    try {
      await deleteOrder(accessToken, orderId);
      if (editingOrder?.id === orderId) {
        setEditingOrder(null);
      }
      await loadOrders();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to delete order");
    }
  }

  const customerLookup = new Map(customers.map((customer) => [customer.id, `${customer.first_name} ${customer.last_name}`]));

  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Workspace</p>
        <h1 className="mt-2 text-3xl font-semibold">Orders</h1>
        <p className="mt-2 text-sm text-muted">Live order list from the FastAPI backend.</p>
      </div>

      <form action={handleCreateOrder} className="glass-panel-strong rounded-3xl p-5">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <select name="customer_id" defaultValue="" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none" required>
            <option value="" disabled>Select customer</option>
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.first_name} {customer.last_name}
              </option>
            ))}
          </select>
          <input name="order_number" placeholder="Order number" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <select name="product_id" defaultValue="" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none" required>
            <option value="" disabled>Select product</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </select>
          <input name="unit_price" placeholder="Unit price" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[180px_180px_1fr]">
          <select name="status" defaultValue="draft" className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
            <option value="draft">Draft</option>
            <option value="confirmed">Confirmed</option>
            <option value="processing">Processing</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <input name="currency" defaultValue="USD" placeholder="Currency" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <input name="quantity" type="number" min="1" defaultValue="1" placeholder="Quantity" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
          <input name="notes" placeholder="Notes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <div className="flex items-end">
            <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
              {isSubmitting ? "Creating..." : "Create order"}
            </button>
          </div>
        </div>
        {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
      </form>

      {editingOrder ? (
        <form action={handleUpdateOrder} className="glass-panel-strong rounded-3xl p-5">
          <input type="hidden" name="order_id" value={editingOrder.id} />
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Editing</p>
              <h2 className="mt-2 text-xl font-semibold">Update order</h2>
            </div>
            <button
              type="button"
              onClick={() => setEditingOrder(null)}
              className="rounded-2xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5"
            >
              Cancel
            </button>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <select name="customer_id" defaultValue={editingOrder.customer_id} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none" required>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.first_name} {customer.last_name}
                </option>
              ))}
            </select>
            <select name="status" defaultValue={editingOrder.status} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="draft">Draft</option>
              <option value="confirmed">Confirmed</option>
              <option value="processing">Processing</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <input name="currency" defaultValue={editingOrder.currency} placeholder="Currency" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
            <input name="notes" defaultValue={editingOrder.notes ?? ""} placeholder="Notes" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <div className="flex items-end">
              <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
                {isSubmitting ? "Updating..." : "Update order"}
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
              <th className="px-5 py-4 font-medium">Order</th>
              <th className="px-5 py-4 font-medium">Customer</th>
              <th className="px-5 py-4 font-medium">Status</th>
              <th className="px-5 py-4 font-medium">Total</th>
              <th className="px-5 py-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((row) => (
              <tr key={row.id} className="border-b border-white/5 last:border-none">
                <td className="px-5 py-4 font-mono text-xs text-slate-300">{row.order_number}</td>
                <td className="px-5 py-4">{customerLookup.get(row.customer_id) ?? `Customer #${row.customer_id}`}</td>
                <td className="px-5 py-4 text-slate-300">{row.status}</td>
                <td className="px-5 py-4 text-slate-300">{row.total_amount}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setEditingOrder(row)}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-slate-100 transition hover:bg-white/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        void handleDeleteOrder(row.id);
                      }}
                      className="rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-100 transition hover:bg-red-500/20"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!orders.length ? (
              <tr>
                <td className="px-5 py-6 text-slate-400" colSpan={5}>
                  No orders returned yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}
