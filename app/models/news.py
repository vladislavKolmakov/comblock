from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True, index=True, nullable=False)
    title: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    short_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    categories: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    views_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comments_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    keywords: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    topic: Mapped[str | None] = mapped_column(String(255), nullable=True)
    has_video: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    enrichment_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    images: Mapped[list["NewsImage"]] = relationship(
        back_populates="news",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class NewsImage(Base):
    __tablename__ = "news_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    news: Mapped[News] = relationship(back_populates="images")
