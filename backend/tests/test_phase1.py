from __future__ import annotations

from decimal import Decimal


def _auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def test_health_check(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_current_user_rejects_invalid_token(client) -> None:
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer definitely-not-a-valid-token"},
    )

    assert response.status_code == 401


def test_auth_and_crud_flow(client) -> None:
    register_payload = {
        "first_name": "Amina",
        "last_name": "Yusuf",
        "email": "amina@example.com",
        "password": "StrongPass123!",
        "role_name": "Sales Executive",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)

    assert register_response.status_code == 201
    register_data = register_response.json()
    access_token = register_data["tokens"]["access_token"]
    refresh_token = register_data["tokens"]["refresh_token"]

    me_response = client.get("/api/v1/users/me", headers=_auth_headers(access_token))
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "amina@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "amina@example.com", "password": "StrongPass123!"},
    )
    assert login_response.status_code == 200

    refresh_response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    assert refresh_response.json()["token_type"] == "bearer"

    customer_response = client.post(
        "/api/v1/customers",
        headers=_auth_headers(access_token),
        json={
            "first_name": "Jordan",
            "last_name": "Lee",
            "email": "jordan@example.com",
            "company_name": "Acme Co",
            "status": "lead",
        },
    )
    assert customer_response.status_code == 201
    customer_id = customer_response.json()["id"]

    product_response = client.post(
        "/api/v1/products",
        headers=_auth_headers(access_token),
        json={
            "name": "Starter CRM Pack",
            "sku": "CRM-001",
            "unit_price": "120.00",
            "stock_quantity": 10,
            "is_active": True,
        },
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    order_response = client.post(
        "/api/v1/orders",
        headers=_auth_headers(access_token),
        json={
            "customer_id": customer_id,
            "order_number": "ORD-1001",
            "status": "draft",
            "currency": "USD",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": "120.00",
                }
            ],
        },
    )
    assert order_response.status_code == 201
    assert Decimal(order_response.json()["total_amount"]) == Decimal("240.00")

    customers_response = client.get("/api/v1/customers", headers=_auth_headers(access_token))
    products_response = client.get("/api/v1/products", headers=_auth_headers(access_token))
    orders_response = client.get("/api/v1/orders", headers=_auth_headers(access_token))

    assert customers_response.status_code == 200
    assert products_response.status_code == 200
    assert orders_response.status_code == 200
    assert len(customers_response.json()) == 1
    assert len(products_response.json()) == 1
    assert len(orders_response.json()) == 1

    logout_response = client.post("/api/v1/auth/logout", headers=_auth_headers(access_token))
    assert logout_response.status_code == 204


def test_sales_executive_cannot_delete_customer(client) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Sam",
            "last_name": "Taylor",
            "email": "sam@example.com",
            "password": "StrongPass123!",
            "role_name": "Sales Executive",
        },
    )
    access_token = register_response.json()["tokens"]["access_token"]

    customer_response = client.post(
        "/api/v1/customers",
        headers=_auth_headers(access_token),
        json={
            "first_name": "Maya",
            "last_name": "Singh",
            "email": "maya@example.com",
            "company_name": "Northwind",
            "status": "lead",
        },
    )
    customer_id = customer_response.json()["id"]

    delete_response = client.delete(f"/api/v1/customers/{customer_id}", headers=_auth_headers(access_token))

    assert delete_response.status_code == 403


def test_admin_can_delete_customer_product_and_order(client) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "StrongPass123!",
            "role_name": "Admin",
        },
    )
    access_token = register_response.json()["tokens"]["access_token"]
    headers = _auth_headers(access_token)

    customer_response = client.post(
        "/api/v1/customers",
        headers=headers,
        json={
            "first_name": "Delete",
            "last_name": "Me",
            "email": "delete-me@example.com",
            "company_name": "Delete Co",
            "status": "lead",
        },
    )
    customer_id = customer_response.json()["id"]

    product_response = client.post(
        "/api/v1/products",
        headers=headers,
        json={
            "name": "Delete Product",
            "sku": "DEL-001",
            "unit_price": "50.00",
            "stock_quantity": 5,
            "is_active": True,
        },
    )
    product_id = product_response.json()["id"]

    order_response = client.post(
        "/api/v1/orders",
        headers=headers,
        json={
            "customer_id": customer_id,
            "order_number": "ORD-DEL-1",
            "status": "draft",
            "currency": "USD",
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                    "unit_price": "50.00",
                }
            ],
        },
    )
    order_id = order_response.json()["id"]

    delete_order_response = client.delete(f"/api/v1/orders/{order_id}", headers=headers)
    delete_product_response = client.delete(f"/api/v1/products/{product_id}", headers=headers)
    delete_customer_response = client.delete(f"/api/v1/customers/{customer_id}", headers=headers)

    assert delete_order_response.status_code == 204
    assert delete_product_response.status_code == 204
    assert delete_customer_response.status_code == 204


def test_admin_can_manage_triggers(client) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "trigger-admin@example.com",
            "password": "StrongPass123!",
            "role_name": "Admin",
        },
    )
    headers = _auth_headers(register_response.json()["tokens"]["access_token"])

    create_response = client.post(
        "/api/v1/triggers",
        headers=headers,
        json={
            "name": "Inactive Customer Follow-up",
            "trigger_type": "inactive_customer",
            "description": "Create a follow-up task when a customer goes inactive",
            "condition_expression": "customer.status == 'inactive'",
            "delay_minutes": 1440,
            "is_active": True,
        },
    )
    trigger_id = create_response.json()["id"]

    list_response = client.get("/api/v1/triggers", headers=headers)
    update_response = client.patch(
        f"/api/v1/triggers/{trigger_id}",
        headers=headers,
        json={"delay_minutes": 720, "is_active": False},
    )
    delete_response = client.delete(f"/api/v1/triggers/{trigger_id}", headers=headers)

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert update_response.status_code == 200
    assert update_response.json()["delay_minutes"] == 720
    assert update_response.json()["is_active"] is False
    assert delete_response.status_code == 204


def test_admin_can_manage_tasks(client) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "task-admin@example.com",
            "password": "StrongPass123!",
            "role_name": "Admin",
        },
    )
    admin_user_id = register_response.json()["user"]["id"]
    headers = _auth_headers(register_response.json()["tokens"]["access_token"])

    customer_response = client.post(
        "/api/v1/customers",
        headers=headers,
        json={
            "first_name": "Task",
            "last_name": "Customer",
            "email": "task-customer@example.com",
            "company_name": "Task Co",
            "status": "active",
        },
    )
    customer_id = customer_response.json()["id"]

    trigger_response = client.post(
        "/api/v1/triggers",
        headers=headers,
        json={
            "name": "Task Trigger",
            "trigger_type": "customer_created",
            "description": "Kick off onboarding task",
            "condition_expression": "customer.status == 'active'",
            "delay_minutes": 60,
            "is_active": True,
        },
    )
    trigger_id = trigger_response.json()["id"]

    create_response = client.post(
        "/api/v1/tasks",
        headers=headers,
        json={
            "customer_id": customer_id,
            "assigned_user_id": admin_user_id,
            "trigger_id": trigger_id,
            "title": "Follow up onboarding",
            "description": "Call the customer after signup",
            "status": "pending",
            "priority": "high",
            "due_date": "2026-07-06T09:00:00",
        },
    )
    task_id = create_response.json()["id"]

    list_response = client.get("/api/v1/tasks", headers=headers)
    update_response = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={"status": "completed", "priority": "urgent"},
    )
    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"
    assert update_response.json()["priority"] == "urgent"
    assert delete_response.status_code == 204
