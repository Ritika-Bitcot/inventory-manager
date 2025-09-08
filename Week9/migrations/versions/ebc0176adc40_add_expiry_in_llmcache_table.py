"""Add expiry in LLMCache table

Revision ID: ebc0176adc40
Revises: 31e484e25787
Create Date: 2025-09-08 15:40:39.680846

"""

from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ebc0176adc40"
down_revision = "31e484e25787"
branch_labels = None
depends_on = None


def upgrade():
    # Add column with default expiry for existing rows
    expires_default = datetime.now(timezone.utc) + timedelta(hours=1)

    with op.batch_alter_table("llm_cache", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "expires_at",
                sa.DateTime(timezone=False),
                nullable=False,
                server_default=sa.text(f"'{expires_default.isoformat()}'"),
            )
        )
        batch_op.create_index(
            batch_op.f("ix_llm_cache_expires_at"), ["expires_at"], unique=False
        )

    # Remove default so model/ORM sets it for new inserts
    op.alter_column("llm_cache", "expires_at", server_default=None)


def downgrade():
    with op.batch_alter_table("llm_cache", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_llm_cache_expires_at"))
        batch_op.drop_column("expires_at")
