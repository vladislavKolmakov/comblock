"""create tables

Revision ID: 0001_create_tables
Revises:
Create Date: 2026-05-31 17:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_create_tables"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("title", sa.String(length=1024), nullable=True),
        sa.Column("source", sa.String(length=255), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("short_text", sa.Text(), nullable=True),
        sa.Column("full_text", sa.Text(), nullable=True),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("categories", sa.Text(), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column("views_count", sa.Integer(), nullable=True),
        sa.Column("comments_count", sa.Integer(), nullable=True),
        sa.Column("keywords", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("region", sa.String(length=255), nullable=True),
        sa.Column("topic", sa.String(length=255), nullable=True),
        sa.Column("has_video", sa.Boolean(), nullable=True),
        sa.Column("enrichment_status", sa.String(length=20), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index(op.f("ix_news_id"), "news", ["id"], unique=False)
    op.create_index(op.f("ix_news_url"), "news", ["url"], unique=False)

    op.create_table(
        "news_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("news_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=2048), nullable=False),
        sa.Column("is_main", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["news_id"], ["news.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_news_images_id"), "news_images", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_news_images_id"), table_name="news_images")
    op.drop_table("news_images")
    op.drop_index(op.f("ix_news_url"), table_name="news")
    op.drop_index(op.f("ix_news_id"), table_name="news")
    op.drop_table("news")
