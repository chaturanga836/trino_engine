from fastapi import FastAPI
from .models import database, user_model
from .routes import auth_routes, health_routes, jwks_routes
from dotenv import load_dotenv
import os
import logging

# --- Load environment variables ---
load_dotenv()

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("trino-auth")

# --- Validate critical environment variables ---
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("❌ DATABASE_URL not set. Please define it in .env or docker-compose.")

logger.info("✅ DATABASE_URL found and loaded successfully")

# --- Initialize FastAPI app ---
app = FastAPI(
    title="Trino Auth Service",
    version="1.0.0",
    description="Handles authentication and integrates with Apache Ranger for Trino authorization."
)

# --- Database initialization ---
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting Trino Auth Service...")
    try:
        user_model.Base.metadata.create_all(bind=database.engine)
        logger.info("✅ Database tables checked/created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

# --- Include route modules ---
app.include_router(health_routes.router)
app.include_router(auth_routes.router)
app.include_router(jwks_routes.router)

# --- Root endpoint ---
@app.get("/")
def root():
    return {
        "status": "Trino Auth Service running",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "dev")
    }
