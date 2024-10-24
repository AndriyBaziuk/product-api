"""create product and category tables

Revision ID: 3c1f0eb79dce
Revises:
Create Date: 2024-10-21 03:11:03.691541

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3c1f0eb79dce"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_category")),
        sa.UniqueConstraint("name", name=op.f("uq_category_name")),
    )
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
            name=op.f("fk_product_category_id_category"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product")),
        sa.UniqueConstraint("name", name=op.f("uq_product_name")),
    )


def downgrade() -> None:
    op.drop_table("product")
    op.drop_table("category")
