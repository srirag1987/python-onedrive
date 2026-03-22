from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    size_kb = Column(Integer)
    item_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)