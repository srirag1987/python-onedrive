from fastapi import FastAPI
from app.database.session import engine
from app.models.base import Base

# IMPORTANT: import models so SQLAlchemy registers them
from app.models import project, country, project_country

from app.api.routes.project_routes import router as project_router

app = FastAPI(title="Async FastAPI Clean Architecture")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(project_router)