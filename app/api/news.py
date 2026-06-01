from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.repositories.news_repository import NewsRepository
from app.schemas.news import EnrichRequest, NewsListResponse, NewsResponse
from app.services.news_enrichment_service import NewsEnrichmentService


router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=NewsListResponse)
async def get_news_list(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
) -> NewsListResponse:
    repository = NewsRepository(session)
    items = await repository.get_news_list(limit=limit, offset=offset)
    return NewsListResponse(items=items)


@router.get("/{news_id}", response_model=NewsResponse)
async def get_news(news_id: int, session: AsyncSession = Depends(get_db_session)) -> NewsResponse:
    repository = NewsRepository(session)
    news = await repository.get_news_by_id(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return NewsResponse.model_validate(news)


@router.post("/enrich")
async def enrich_news(payload: EnrichRequest, background_tasks: BackgroundTasks) -> dict:
    service = NewsEnrichmentService()
    background_tasks.add_task(service.enrich_news, payload.urls)
    return {"status": "accepted", "message": "Enrichment started"}
