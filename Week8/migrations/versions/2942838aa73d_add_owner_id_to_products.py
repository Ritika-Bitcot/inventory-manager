"""Add owner_id to products

Revision ID: 2942838aa73d
Revises: 930c26bfce9f
Create Date: 2025-08-29 16:20:34.353627

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2942838aa73d"
down_revision = "930c26bfce9f"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: add column as nullable
    op.add_column(
        "products", sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.create_foreign_key(
        "fk_products_owner_id_users", "products", "users", ["owner_id"], ["id"]
    )

    # Step 2: backfill with existing admin
    conn = op.get_bind()
    admin_id = conn.execute(
        sa.text("SELECT id FROM users WHERE role='admin' LIMIT 1")
    ).scalar()
    if admin_id:
        conn.execute(
            sa.text("UPDATE products SET owner_id = :admin_id"), {"admin_id": admin_id}
        )

    # Step 3: enforce NOT NULL after backfilling
    op.alter_column("products", "owner_id", nullable=False)


def downgrade():
    op.drop_constraint("fk_products_owner_id_users", "products", type_="foreignkey")
    op.drop_column("products", "owner_id")
