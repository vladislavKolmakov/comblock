from app.database.session import AsyncSessionLocal
from app.parsers.ria_parser import RiaParser
from app.repositories.news_repository import NewsRepository


class NewsEnrichmentService:
    def __init__(self) -> None:
        self.parser = RiaParser()

    async def enrich_news(self, urls: list[str]) -> None:
        async with AsyncSessionLocal() as session:
            repository = NewsRepository(session)

            for url in urls:
                try:
                    html = await self.parser.fetch_html(url)
                    parsed = self.parser.parse_article(html)

                    payload = {
                        "url": url,
                        "title": parsed.get("title"),
                        "source": "ria.ru",
                        "published_at": parsed.get("published_at"),
                        "full_text": parsed.get("full_text"),
                        "author": parsed.get("author"),
                        "enrichment_status": "SUCCESS",
                        "error_message": None,
                    }

                    existing_news = await repository.get_news_by_url(url)
                    if existing_news:
                        news = await repository.update_news(existing_news, payload)
                    else:
                        news = await repository.create_news(payload)

                    await repository.replace_images(news, parsed.get("image_urls", []))
                    await session.commit()
                except Exception as exc:
                    existing_news = await repository.get_news_by_url(url)
                    error_payload = {
                        "source": "ria.ru",
                        "enrichment_status": "FAILED",
                        "error_message": str(exc),
                    }
                    if existing_news:
                        await repository.update_news(existing_news, error_payload)
                    else:
                        await repository.create_news(
                            {"url": url, **error_payload}
                        )
                    await session.commit()
