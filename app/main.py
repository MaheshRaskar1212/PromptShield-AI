
from fastapi import FastAPI
from app.core.middleware import RequestSizeLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as security_test_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI application security testing platform",
    version=settings.app_version,
)

app.add_middleware(RequestSizeLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(security_test_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PromptShield AI",
        "version": settings.app_version,
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "promptshield-ai",
        "version": settings.app_version,
    }
