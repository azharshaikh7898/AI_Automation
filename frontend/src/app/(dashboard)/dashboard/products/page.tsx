"use client";

import { useCallback, useEffect, useState } from "react";
import { createProduct, deleteProduct, fetchProducts, updateProduct } from "@/services/products";
import { useAuth } from "@/hooks/useAuth";
import type { ProductCreatePayload, ProductRead } from "@/lib/types";

export default function ProductsPage() {
  const { accessToken, isHydrated } = useAuth();
  const [products, setProducts] = useState<ProductRead[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [editingProduct, setEditingProduct] = useState<ProductRead | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadProducts = useCallback(async () => {
    if (!accessToken) {
      return;
    }

    const productList = await fetchProducts(accessToken);
    setProducts(productList);
  }, [accessToken]);

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    loadProducts()
      .catch(() => setProducts([]));
  }, [accessToken, isHydrated, loadProducts]);

  async function handleCreateProduct(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const payload: ProductCreatePayload = {
      name: String(formData.get("name") ?? "").trim(),
      sku: String(formData.get("sku") ?? "").trim(),
      description: String(formData.get("description") ?? "").trim() || null,
      unit_price: String(formData.get("unit_price") ?? "0.00").trim(),
      stock_quantity: Number(formData.get("stock_quantity") ?? 0),
      is_active: true,
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await createProduct(accessToken, payload);
      await loadProducts();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to create product");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleUpdateProduct(formData: FormData) {
    if (!accessToken) {
      return;
    }

    const productId = Number(formData.get("product_id") ?? 0);
    const payload: ProductCreatePayload = {
      name: String(formData.get("name") ?? "").trim(),
      sku: String(formData.get("sku") ?? "").trim(),
      description: String(formData.get("description") ?? "").trim() || null,
      unit_price: String(formData.get("unit_price") ?? "0.00").trim(),
      stock_quantity: Number(formData.get("stock_quantity") ?? 0),
      is_active: String(formData.get("is_active") ?? "true") === "true",
    };

    setIsSubmitting(true);
    setError(null);
    try {
      await updateProduct(accessToken, productId, payload);
      setEditingProduct(null);
      await loadProducts();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to update product");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteProduct(productId: number) {
    if (!accessToken) {
      return;
    }

    if (!window.confirm("Delete this product?")) {
      return;
    }

    setError(null);
    try {
      await deleteProduct(accessToken, productId);
      if (editingProduct?.id === productId) {
        setEditingProduct(null);
      }
      await loadProducts();
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to delete product");
    }
  }

  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-sky-300/80">Workspace</p>
        <h1 className="mt-2 text-3xl font-semibold">Products</h1>
        <p className="mt-2 text-sm text-muted">Live product catalog from the FastAPI backend.</p>
      </div>

      <form action={handleCreateProduct} className="glass-panel-strong rounded-3xl p-5">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <input name="name" placeholder="Product name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <input name="sku" placeholder="SKU" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <input name="unit_price" placeholder="Unit price" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
          <input name="stock_quantity" type="number" min="0" defaultValue="0" placeholder="Stock" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
          <input name="description" placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          <div className="flex items-end">
            <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
              {isSubmitting ? "Creating..." : "Create product"}
            </button>
          </div>
        </div>
        {error ? <p className="mt-4 rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">{error}</p> : null}
      </form>

      {editingProduct ? (
        <form action={handleUpdateProduct} className="glass-panel-strong rounded-3xl p-5">
          <input type="hidden" name="product_id" value={editingProduct.id} />
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Editing</p>
              <h2 className="mt-2 text-xl font-semibold">Update product</h2>
            </div>
            <button
              type="button"
              onClick={() => setEditingProduct(null)}
              className="rounded-2xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/5"
            >
              Cancel
            </button>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <input name="name" defaultValue={editingProduct.name} placeholder="Product name" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <input name="sku" defaultValue={editingProduct.sku} placeholder="SKU" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <input name="unit_price" defaultValue={editingProduct.unit_price} placeholder="Unit price" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" required />
            <input name="stock_quantity" type="number" min="0" defaultValue={editingProduct.stock_quantity} placeholder="Stock" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-[1fr_220px_auto]">
            <input name="description" defaultValue={editingProduct.description ?? ""} placeholder="Description" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 outline-none" />
            <select name="is_active" defaultValue={String(editingProduct.is_active)} className="rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 outline-none">
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
            <div className="flex items-end">
              <button type="submit" disabled={isSubmitting} className="rounded-2xl bg-amber-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-70">
                {isSubmitting ? "Updating..." : "Update product"}
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
              <th className="px-5 py-4 font-medium">SKU</th>
              <th className="px-5 py-4 font-medium">Product</th>
              <th className="px-5 py-4 font-medium">Price</th>
              <th className="px-5 py-4 font-medium">Stock</th>
              <th className="px-5 py-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((row) => (
              <tr key={row.id} className="border-b border-white/5 last:border-none">
                <td className="px-5 py-4 font-mono text-xs text-slate-300">{row.sku}</td>
                <td className="px-5 py-4">{row.name}</td>
                <td className="px-5 py-4 text-slate-300">{row.unit_price}</td>
                <td className="px-5 py-4 text-slate-300">{row.stock_quantity}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => setEditingProduct(row)}
                      className="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-slate-100 transition hover:bg-white/10"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        void handleDeleteProduct(row.id);
                      }}
                      className="rounded-xl border border-red-400/30 bg-red-500/10 px-3 py-2 text-xs font-semibold text-red-100 transition hover:bg-red-500/20"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!products.length ? (
              <tr>
                <td className="px-5 py-6 text-slate-400" colSpan={5}>
                  No products returned yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}
