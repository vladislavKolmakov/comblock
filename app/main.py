from fastapi import FastAPI

from app.api.news import router as news_router


app = FastAPI(title="News Parser Service")
app.include_router(news_router)
