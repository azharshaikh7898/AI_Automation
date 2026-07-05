"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { fetchCustomers } from "@/services/customers";
import { fetchOrders } from "@/services/orders";
import { fetchProducts } from "@/services/products";

export default function DashboardPage() {
  const { accessToken, isHydrated } = useAuth();
  const [customersCount, setCustomersCount] = useState<number>(0);
  const [productsCount, setProductsCount] = useState<number>(0);
  const [ordersCount, setOrdersCount] = useState<number>(0);
  const [latestRevenue, setLatestRevenue] = useState<string>("0.00");

  useEffect(() => {
    if (!isHydrated || !accessToken) {
      return;
    }

    Promise.all([
      fetchCustomers(accessToken),
      fetchProducts(accessToken),
      fetchOrders(accessToken),
    ])
      .then(([customerList, productList, orderList]) => {
        setCustomersCount(customerList.length);
        setProductsCount(productList.length);
        setOrdersCount(orderList.length);
        const revenue = orderList.reduce((total, order) => total + Number(order.total_amount), 0);
        setLatestRevenue(revenue.toFixed(2));
      })
      .catch(() => {
        setCustomersCount(0);
        setProductsCount(0);
        setOrdersCount(0);
        setLatestRevenue("0.00");
      });
  }, [accessToken, isHydrated]);

  const stats = [
    { label: "Customers", value: customersCount.toString() },
    { label: "Products", value: productsCount.toString() },
    { label: "Orders", value: ordersCount.toString() },
    { label: "Revenue", value: `$${latestRevenue}` },
  ];

  const quickLinks = [
    { title: "Customers", description: "Track customer status, ownership, and follow-up history." },
    { title: "Products", description: "Manage catalog items, pricing, and inventory signals." },
    { title: "Orders", description: "Review quotations, fulfillment state, and payments." },
  ];

  return (
    <div className="space-y-8">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((item) => (
          <div key={item.label} className="rounded-3xl border border-white/10 bg-white/5 p-5">
            <p className="text-sm text-muted">{item.label}</p>
            <p className="mt-3 text-3xl font-semibold">{item.value}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-4 xl:grid-cols-3">
        {quickLinks.map((item) => (
          <article key={item.title} className="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
            <h2 className="text-xl font-semibold">{item.title}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-300">{item.description}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
