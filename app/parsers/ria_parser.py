from datetime import datetime

import httpx
from bs4 import BeautifulSoup


class RiaParser:
    async def fetch_html(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    def parse_article(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else None

        author_tag = soup.select_one('[itemprop="author"]')
        if not author_tag:
            author_tag = soup.select_one(".article__authors-name")
        author = author_tag.get_text(strip=True) if author_tag else None

        datetime_tag = soup.find("time")
        published_at = self._parse_datetime(datetime_tag.get("datetime")) if datetime_tag else None

        paragraphs = soup.select(".article__text")
        if not paragraphs:
            paragraphs = soup.select('[itemprop="articleBody"] p')
        full_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)) or None

        image_tags = soup.select("img")
        image_urls: list[str] = []
        for image in image_tags:
            src = image.get("src") or image.get("data-src")
            if src and src.startswith("http"):
                image_urls.append(src)
        # Preserve order but remove duplicates.
        image_urls = list(dict.fromkeys(image_urls))

        return {
            "title": title,
            "full_text": full_text,
            "author": author,
            "published_at": published_at,
            "image_urls": image_urls,
        }

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
