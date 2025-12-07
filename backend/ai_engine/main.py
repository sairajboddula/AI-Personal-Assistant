from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ai_engine.app.routers import chat
from backend.ai_engine.app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "AI Engine is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

