from fastapi import FastAPI
from .models import database, user_model
from .routes import auth_routes, health_routes

# Create tables if not exist
user_model.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Trino Auth Service", version="1.0.0")

app.include_router(health_routes.router, prefix="")
app.include_router(auth_routes.router, prefix="/auth")
