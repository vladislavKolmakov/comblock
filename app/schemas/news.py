from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsImageResponse(BaseModel):
    id: int
    image_url: str
    is_main: bool

    model_config = ConfigDict(from_attributes=True)


class NewsResponse(BaseModel):
    id: int
    url: str
    title: str | None
    source: str | None
    published_at: datetime | None
    short_text: str | None
    full_text: str | None
    author: str | None
    categories: str | None
    tags: str | None
    views_count: int | None
    comments_count: int | None
    keywords: str | None
    summary: str | None
    region: str | None
    topic: str | None
    has_video: bool | None
    enrichment_status: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    images: list[NewsImageResponse]

    model_config = ConfigDict(from_attributes=True)


class NewsListResponse(BaseModel):
    items: list[NewsResponse]


class EnrichRequest(BaseModel):
    urls: list[str]
