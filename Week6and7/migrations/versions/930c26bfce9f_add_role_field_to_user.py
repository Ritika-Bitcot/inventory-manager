"""add role field to user

Revision ID: 930c26bfce9f
Revises: a097c1005b66
Create Date: 2025-08-29 12:16:06.909255

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "930c26bfce9f"
down_revision = "a097c1005b66"
branch_labels = None
depends_on = None


def upgrade():
    user_roles = sa.Enum("admin", "manager", "staff", name="user_roles")
    user_roles.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("role", user_roles, nullable=False, server_default="staff")
        )
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("role")

    user_roles = sa.Enum("admin", "manager", "staff", name="user_roles")
    user_roles.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
