from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import (AppException, app_exception_handler, generic_exception_handler,)
from app.models.message import Message

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app using config
app = FastAPI(
    title="ACB AI",
    description="Autonomous AI Agent Backend",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "ACB AI Backend Running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ACB AI Backend",
    }