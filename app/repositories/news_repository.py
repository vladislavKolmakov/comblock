from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import News, NewsImage


class NewsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_news(self, payload: dict) -> News:
        news = News(**payload)
        self.session.add(news)
        await self.session.flush()
        await self.session.refresh(news)
        return news

    async def get_news_by_id(self, news_id: int) -> News | None:
        query = (
            select(News)
            .options(selectinload(News.images))
            .where(News.id == news_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_news_by_url(self, url: str) -> News | None:
        query = (
            select(News)
            .options(selectinload(News.images))
            .where(News.url == url)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_news_list(self, limit: int = 20, offset: int = 0) -> list[News]:
        query = (
            select(News)
            .options(selectinload(News.images))
            .order_by(News.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_news(self, news: News, payload: dict) -> News:
        for key, value in payload.items():
            setattr(news, key, value)
        await self.session.flush()
        await self.session.refresh(news)
        return news

    async def replace_images(self, news: News, image_urls: list[str]) -> None:
        news.images.clear()
        for index, image_url in enumerate(image_urls):
            news.images.append(NewsImage(image_url=image_url, is_main=index == 0))
        await self.session.flush()
