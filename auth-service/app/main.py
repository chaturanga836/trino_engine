from fastapi import FastAPI
from .models import database, user_model
from .routes import auth_routes, health_routes
from dotenv import load_dotenv
import os

# Load environment variables from .env (useful for local development)
load_dotenv()

# Ensure database URL is set before starting
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("❌ DATABASE_URL not set. Please define it in .env or docker-compose.")

# Initialize FastAPI app
app = FastAPI(
    title="Trino Auth Service",
    version="1.0.0",
    description="Handles authentication and integrates with Apache Ranger for Trino authorization."
)

# Create tables if they don't exist
user_model.Base.metadata.create_all(bind=database.engine)

# Include route modules
app.include_router(health_routes.router, prefix="")
app.include_router(auth_routes.router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "Trino Auth Service running", "version": "1.0.0"}
