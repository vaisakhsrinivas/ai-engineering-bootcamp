from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from app.routes import health, summarize, sentiment

load_dotenv()

app = FastAPI(
    title="AI Engineering Bootcamp API",
    description="Health check, summarization, and sentiment analysis with multiple prompt strategies",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(summarize.router, prefix="/summarize", tags=["summarize"])
app.include_router(sentiment.router, prefix="/analyze-sentiment", tags=["sentiment"])
