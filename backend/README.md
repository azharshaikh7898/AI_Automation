# Customer Retention & Sales Automation API

Phase 1 backend for an AI-powered customer retention and sales automation system.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- JWT authentication
- bcrypt password hashing
- Pydantic v2
- python-dotenv

## Current Backend Scope

- Health check endpoint
- Versioned API routing
- CORS configuration
- Structured logging
- JWT register/login/refresh/logout flows
- Current user endpoint
- Role seeding for Admin, Manager, and Sales Executive
- Normalized PostgreSQL schema via Alembic

## Environment Setup

Copy the example environment file and update secrets for your environment.

```bash
cp .env.example .env
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
alembic upgrade head
```

## Start the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/me`
- `GET|POST|PATCH|DELETE /api/v1/customers`
- `GET|POST|PATCH|DELETE /api/v1/products`
- `GET|POST|PATCH|DELETE /api/v1/orders`
- `GET|POST|PATCH|DELETE /api/v1/triggers`
- `GET|POST|PATCH|DELETE /api/v1/tasks`
