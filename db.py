from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_SERVER}/{DB_DATABASE}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    return SessionLocal()