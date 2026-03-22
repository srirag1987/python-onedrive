from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

Base = declarative_base()


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    size_kb = Column(Integer)
    item_type = Column(String)  # FILE / FOLDER
    created_at = Column(DateTime, default=datetime.utcnow)