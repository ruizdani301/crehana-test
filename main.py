from fastapi import FastAPI
from infrastructure.api.task_routes import router as task_router
from infrastructure.api.user_routes import router_users as users_router
from infrastructure.db.database import engine
from infrastructure.db.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TASK_TRACKING API", version="1.0.0")

# Endpoints definitions
app.include_router(task_router)
app.include_router(users_router)
