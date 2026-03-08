from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_repository import ProjectRepository


class ProjectService:

    def __init__(self):
        self.repo = ProjectRepository()

    async def create_project(self, db: AsyncSession, name: str):
        return await self.repo.create_project(db, name)

    async def get_projects(self, db: AsyncSession):
        return await self.repo.get_projects(db)