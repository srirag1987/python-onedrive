from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.project import Project


class ProjectRepository:

    async def create_project(self, db: AsyncSession, name: str):

        project = Project(project_name=name)

        db.add(project)

        await db.commit()
        await db.refresh(project)

        return project

    async def get_projects(self, db: AsyncSession):

        result = await db.execute(select(Project))

        return result.scalars().all()