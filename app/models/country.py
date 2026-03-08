from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base


class Country(Base):

    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    projects = relationship(
        "Project",
        secondary="project_countries",
        back_populates="countries"
    )