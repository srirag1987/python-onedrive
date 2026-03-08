from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base


class ProjectCountry(Base):

    __tablename__ = "project_countries"

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id"),
        primary_key=True
    )

    country_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("countries.id"),
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)