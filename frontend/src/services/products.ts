import { apiFetch } from "./api";
import type { ProductCreatePayload, ProductRead } from "@/lib/types";

export function fetchProducts(token: string, offset = 0, limit = 100) {
  return apiFetch<ProductRead[]>(`/products?offset=${offset}&limit=${limit}`, {
    method: "GET",
    token,
  });
}

export function createProduct(token: string, payload: ProductCreatePayload) {
  return apiFetch<ProductRead>("/products", {
    method: "POST",
    token,
    body: JSON.stringify(payload),
  });
}

export function updateProduct(token: string, productId: number, payload: Partial<ProductCreatePayload>) {
  return apiFetch<ProductRead>(`/products/${productId}`, {
    method: "PATCH",
    token,
    body: JSON.stringify(payload),
  });
}

export function deleteProduct(token: string, productId: number) {
  return apiFetch<void>(`/products/${productId}`, {
    method: "DELETE",
    token,
  });
}
