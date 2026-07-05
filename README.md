# Customer Sales Platform

Phase 1 of an AI-powered customer retention and sales automation system.

## Stack

- Backend: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, JWT, Passlib, Pydantic v2
- Frontend: Next.js 15, React, TypeScript, Tailwind CSS
- Infra: Docker Compose

## What is included

- JWT authentication with register, login, refresh, current-user, and logout
- Role-based access control for Admin, Manager, and Sales Executive
- Normalized PostgreSQL schema for users, roles, customers, products, orders, order_items, payments, invoices, interactions, triggers, and tasks
- FastAPI health checks, global exception handling, logging, CORS, and versioned API routing
- Next.js app shell with login, register, protected dashboard, sidebar, and role-aware session handling
- Docker Compose stack for backend, frontend, and PostgreSQL

## Local setup

1. Copy the environment file.
2. Start PostgreSQL.
3. Run Alembic migrations.
4. Start backend and frontend.

```bash
cp .env.example .env
docker compose up --build
```

## Backend

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## API endpoints

- `GET /health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/me`
- `GET|POST|PATCH|DELETE /api/v1/customers`
- `GET|POST|PATCH|DELETE /api/v1/products`
- `GET|POST|PATCH|DELETE /api/v1/orders`
- `GET|POST|PATCH|DELETE /api/v1/triggers` (Admin, Manager)
- `GET|POST|PATCH|DELETE /api/v1/tasks` (all roles; delete restricted to Admin/Manager)

## Tests

```bash
cd backend
pytest
```
