import asyncio
import traceback
from contextlib import asynccontextmanager

from app.api.chat import router as chat_router
from app.api.execute import router as execute_router
from app.api.execution_history import router as execution_history_router
from app.api.file import router as file_router
from app.api.health import router as health_router
from app.api.me import router as me_router
from app.api.metrics import router as metrics_router
from app.api.planner import router as planner_router
from app.api.terminal import router as terminal_router
from app.api.websocket import router as websocket_router
from app.core import event_loop as event_loop_module
from app.core import event_loop as loop_holder
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    file_exists_handler,
    file_not_found_handler,
    value_error_handler,
)
from app.core.logger import logger
from app.execution.events.global_publisher import execution_event_publisher
from app.execution.events.subscribers.logging_subscriber import LoggingSubscriber
from app.execution.events.subscribers.websocket_subscriber import WebSocketSubscriber
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ACB AI Backend")

    # Store FastAPI's running event loop
    event_loop_module.event_loop = asyncio.get_running_loop()

    logger.info(
        "Stored event loop %s",
        loop_holder.event_loop,
    )
    execution_event_publisher.subscribe(LoggingSubscriber())

    execution_event_publisher.subscribe(WebSocketSubscriber())

    yield

    logger.info("Shutting down ACB AI Backend")


app = FastAPI(
    title="ACB AI",
    description="Autonomous AI Agent Backend",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(FileNotFoundError, file_not_found_handler)
app.add_exception_handler(FileExistsError, file_exists_handler)
app.add_exception_handler(ValueError, value_error_handler)


@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    traceback.print_exc()
    raise exc


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat_router)
app.include_router(planner_router)
app.include_router(file_router)
app.include_router(terminal_router)
app.include_router(execute_router)
app.include_router(execution_history_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(me_router)
app.include_router(websocket_router)


@app.get("/")
def home():
    return {
        "message": "ACB AI Backend Running",
        "status": "success",
    }
