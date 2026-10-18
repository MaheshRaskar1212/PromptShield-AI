
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as security_test_router

app = FastAPI(
    title="PromptShield AI",
    description="AI application security testing platform",
    version="0.1.0",
)

# Temporary local-development configuration.
# Restrict origins before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(security_test_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PromptShield AI",
        "version": "0.1.0",
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "promptshield-ai",
        "version": "0.1.0",
    }
