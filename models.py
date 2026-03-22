from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    web_url = Column(String)
    created_at_graph = Column(DateTime)
    last_modified = Column(DateTime)

    # optional: store full raw JSON
    raw_json = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    countries = relationship(
        "Country",
        secondary="project_countries",
        back_populates="projects"
    )


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    projects = relationship(
        "Project",
        secondary="project_countries",
        back_populates="countries"
    )


class ProjectCountry(Base):
    __tablename__ = "project_countries"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), primary_key=True)