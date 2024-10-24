"""add image_url column to product table

Revision ID: 839dbfd27638
Revises: 3c1f0eb79dce
Create Date: 2024-10-23 01:10:33.387997

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "839dbfd27638"
down_revision: Union[str, None] = "3c1f0eb79dce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("product", sa.Column("image_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("product", "image_url")
