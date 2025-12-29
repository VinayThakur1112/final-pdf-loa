import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

from app.common.logging import get_logger

logger = get_logger(__name__)

load_dotenv()

# logger.info(f"DB_USER: {os.getenv('DB_USER')}")
# logger.info(f"DB_HOST: {os.getenv('DB_HOST')}")
# logger.info(f"DB_NAME: {os.getenv('DB_NAME')}")
# logger.info(f"DB_PORT: {os.getenv('DB_PORT')}")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)