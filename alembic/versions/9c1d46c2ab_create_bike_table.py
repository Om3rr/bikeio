"""create bike table

Revision ID: 9c1d46c2ab
Revises: 
Create Date: 2021-03-10 22:39:31.751123

"""

# revision identifiers, used by Alembic.
revision = '9c1d46c2ab'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table("bike",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("bike_id", sa.String(255), unique=True, index=True, nullable=False),
                    sa.Column("first_name", sa.String(255)),
                    sa.Column("last_name", sa.String(255)),
                    sa.Column("color", sa.String(255)),
                    sa.Column("brand", sa.String(255)),
                    sa.Column("city", sa.String(255)),
                    sa.Column("phone", sa.String(255)),
                    sa.Column("secondary_phone", sa.String(255)),
                    sa.Column("assets", sa.JSON),
                    sa.Column("created_at", sa.DateTime),
                    )


def downgrade():
    op.drop_table("bike")
