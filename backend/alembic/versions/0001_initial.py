"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-04 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("stock_quantity >= 0", name=op.f("ck_products_products_stock_quantity_non_negative")),
        sa.CheckConstraint("unit_price >= 0", name=op.f("ck_products_products_unit_price_non_negative")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("sku", name=op.f("uq_products_sku")),
    )
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=False)

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roles")),
        sa.UniqueConstraint("name", name=op.f("uq_roles_name")),
    )
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=False)

    op.create_table(
        "triggers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("trigger_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("condition_expression", sa.Text(), nullable=True),
        sa.Column("delay_minutes", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "delay_minutes >= 0",
            name=op.f("ck_triggers_triggers_delay_minutes_non_negative"),
        ),
        sa.CheckConstraint(
            "trigger_type IN ('customer_created', 'order_created', 'payment_failed', 'invoice_overdue', 'inactive_customer')",
            name=op.f("ck_triggers_triggers_type_valid"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_triggers")),
        sa.UniqueConstraint("name", name=op.f("uq_triggers_name")),
    )
    op.create_index(op.f("ix_triggers_name"), "triggers", ["name"], unique=False)
    op.create_index(op.f("ix_triggers_trigger_type"), "triggers", ["trigger_type"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("is_superuser", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name=op.f("fk_users_role_id_roles"), ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_users_phone_number")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_phone_number"), "users", ["phone_number"], unique=False)

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("assigned_user_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="lead", nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "status IN ('lead', 'prospect', 'active', 'inactive', 'churned')",
            name=op.f("ck_customers_customer_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["assigned_user_id"],
            ["users.id"],
            name=op.f("fk_customers_assigned_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customers")),
    )
    op.create_index(op.f("ix_customers_assigned_user_id_status"), "customers", ["assigned_user_id", "status"], unique=False)
    op.create_index(op.f("ix_customers_company_name"), "customers", ["company_name"], unique=False)
    op.create_index(op.f("ix_customers_email"), "customers", ["email"], unique=False)
    op.create_index(op.f("ix_customers_phone_number"), "customers", ["phone_number"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("order_number", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="draft", nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="USD", nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), server_default="0.00", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft', 'confirmed', 'processing', 'completed', 'cancelled')",
            name=op.f("ck_orders_orders_status_valid"),
        ),
        sa.CheckConstraint("total_amount >= 0", name=op.f("ck_orders_orders_total_amount_non_negative")),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_orders_created_by_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_orders_customer_id_customers"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
        sa.UniqueConstraint("order_number", name=op.f("uq_orders_order_number")),
    )
    op.create_index(op.f("ix_orders_created_by_id_status"), "orders", ["created_by_id", "status"], unique=False)
    op.create_index(op.f("ix_orders_customer_id_status"), "orders", ["customer_id", "status"], unique=False)
    op.create_index(op.f("ix_orders_order_number"), "orders", ["order_number"], unique=False)

    op.create_table(
        "interactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("interaction_type", sa.String(length=20), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("outcome", sa.String(length=255), nullable=True),
        sa.Column("interaction_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "interaction_type IN ('call', 'email', 'meeting', 'sms', 'note')",
            name=op.f("ck_interactions_interactions_type_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["users.id"],
            name=op.f("fk_interactions_created_by_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_interactions_customer_id_customers"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_interactions")),
    )
    op.create_index(
        op.f("ix_interactions_created_by_id_interaction_type"),
        "interactions",
        ["created_by_id", "interaction_type"],
        unique=False,
    )
    op.create_index(op.f("ix_interactions_customer_id_interaction_date"), "interactions", ["customer_id", "interaction_date"], unique=False)
    op.create_index(op.f("ix_interactions_interaction_date"), "interactions", ["interaction_date"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("assigned_user_id", sa.Integer(), nullable=True),
        sa.Column("trigger_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("priority", sa.String(length=20), server_default="medium", nullable=False),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name=op.f("ck_tasks_tasks_priority_valid"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'cancelled')",
            name=op.f("ck_tasks_tasks_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["assigned_user_id"],
            ["users.id"],
            name=op.f("fk_tasks_assigned_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_tasks_customer_id_customers"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["trigger_id"],
            ["triggers.id"],
            name=op.f("fk_tasks_trigger_id_triggers"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )
    op.create_index(op.f("ix_tasks_assigned_user_id_status"), "tasks", ["assigned_user_id", "status"], unique=False)
    op.create_index(op.f("ix_tasks_customer_id_due_date"), "tasks", ["customer_id", "due_date"], unique=False)
    op.create_index(op.f("ix_tasks_due_date"), "tasks", ["due_date"], unique=False)

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("invoice_number", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="draft", nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("amount_due", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("amount_due >= 0", name=op.f("ck_invoices_invoices_amount_due_non_negative")),
        sa.CheckConstraint(
            "status IN ('draft', 'issued', 'paid', 'overdue', 'cancelled')",
            name=op.f("ck_invoices_invoices_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_invoices_order_id_orders"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoices")),
        sa.UniqueConstraint("invoice_number", name=op.f("uq_invoices_invoice_number")),
    )
    op.create_index(op.f("ix_invoices_due_date"), "invoices", ["due_date"], unique=False)
    op.create_index(op.f("ix_invoices_due_date_status"), "invoices", ["due_date", "status"], unique=False)
    op.create_index(op.f("ix_invoices_invoice_number"), "invoices", ["invoice_number"], unique=False)
    op.create_index(op.f("ix_invoices_order_id_status"), "invoices", ["order_id", "status"], unique=False)

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), server_default="pending", nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("transaction_reference", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("amount >= 0", name=op.f("ck_payments_payments_amount_non_negative")),
        sa.CheckConstraint(
            "status IN ('pending', 'authorized', 'paid', 'failed', 'refunded')",
            name=op.f("ck_payments_payments_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_payments_order_id_orders"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payments")),
    )
    op.create_index(op.f("ix_payments_order_id_status"), "payments", ["order_id", "status"], unique=False)
    op.create_index(op.f("ix_payments_payment_method"), "payments", ["payment_method"], unique=False)
    op.create_index(op.f("ix_payments_transaction_reference"), "payments", ["transaction_reference"], unique=False)

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("line_total", sa.Numeric(precision=12, scale=2), server_default="0.00", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("line_total >= 0", name=op.f("ck_order_items_order_items_line_total_non_negative")),
        sa.CheckConstraint("quantity > 0", name=op.f("ck_order_items_order_items_quantity_positive")),
        sa.CheckConstraint("unit_price >= 0", name=op.f("ck_order_items_order_items_unit_price_non_negative")),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_order_items_order_id_orders"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_order_items_product_id_products"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order_items")),
    )
    op.create_index(op.f("ix_order_items_order_id_product_id"), "order_items", ["order_id", "product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_order_items_order_id_product_id"), table_name="order_items")
    op.drop_table("order_items")

    op.drop_index(op.f("ix_payments_transaction_reference"), table_name="payments")
    op.drop_index(op.f("ix_payments_payment_method"), table_name="payments")
    op.drop_index(op.f("ix_payments_order_id_status"), table_name="payments")
    op.drop_table("payments")

    op.drop_index(op.f("ix_invoices_order_id_status"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_invoice_number"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_due_date_status"), table_name="invoices")
    op.drop_index(op.f("ix_invoices_due_date"), table_name="invoices")
    op.drop_table("invoices")

    op.drop_index(op.f("ix_tasks_due_date"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_customer_id_due_date"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_assigned_user_id_status"), table_name="tasks")
    op.drop_table("tasks")

    op.drop_index(op.f("ix_interactions_interaction_date"), table_name="interactions")
    op.drop_index(op.f("ix_interactions_customer_id_interaction_date"), table_name="interactions")
    op.drop_index(op.f("ix_interactions_created_by_id_interaction_type"), table_name="interactions")
    op.drop_table("interactions")

    op.drop_index(op.f("ix_orders_order_number"), table_name="orders")
    op.drop_index(op.f("ix_orders_customer_id_status"), table_name="orders")
    op.drop_index(op.f("ix_orders_created_by_id_status"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(op.f("ix_customers_phone_number"), table_name="customers")
    op.drop_index(op.f("ix_customers_email"), table_name="customers")
    op.drop_index(op.f("ix_customers_company_name"), table_name="customers")
    op.drop_index(op.f("ix_customers_assigned_user_id_status"), table_name="customers")
    op.drop_table("customers")

    op.drop_index(op.f("ix_users_phone_number"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_triggers_trigger_type"), table_name="triggers")
    op.drop_index(op.f("ix_triggers_name"), table_name="triggers")
    op.drop_table("triggers")

    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_table("roles")

    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
