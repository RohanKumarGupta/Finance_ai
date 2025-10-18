from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .db import connect_to_mongo, close_mongo_connection, check_mongo_connection
from .auth.routes import router as auth_router
from .dashboard.routes import router as dashboard_router
from .payments.routes import router as payments_router
from .ai.routes import router as ai_router
from .reminders.routes import router as reminders_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Finance AI Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.on_event("startup")
async def startup():
    logger.info("Starting Finance AI Assistant backend...")
    await connect_to_mongo()
    logger.info("Database connected successfully")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down Finance AI Assistant backend...")
    await close_mongo_connection()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])
app.include_router(reminders_router, prefix="/reminders", tags=["reminders"])

@app.get("/")
async def root():
    return {"status": "ok", "service": app.title, "version": app.version}

@app.get("/health")
async def health_check():
    """Health check endpoint that verifies database connectivity."""
    try:
        db_healthy = await check_mongo_connection()
        logger.info(f"Health check - Database connected: {db_healthy}")

        if db_healthy:
            return {
                "status": "healthy",
                "database": "connected",
                "database_name": settings.DATABASE_NAME,
                "service": app.title,
                "version": app.version
            }
        else:
            logger.warning("Health check failed - Database not connected")
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "service": app.title,
                "version": app.version
            }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "database": "error",
            "service": app.title,
            "version": app.version
        }
