from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.project_schema import ProjectCreate
from app.services.project_service import ProjectService

router = APIRouter()

service = ProjectService()


@router.post("/projects")
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_project(db, project.project_name)


@router.get("/projects")
async def get_projects(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_projects(db)