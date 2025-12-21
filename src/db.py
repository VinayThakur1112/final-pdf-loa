from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from src.config import Config

Base = declarative_base()

class ExtractedData(Base):
    __tablename__ = 'extracted_data'

    id = Column(Integer, primary_key=True)
    source_email_id = Column(String(255), nullable=True)
    sender = Column(String(255), nullable=True)
    subject = Column(Text, nullable=True)
    pdf_filename = Column(String(255), nullable=True)
    extracted_text = Column(Text, nullable=True)
    extracted_json = Column(Text, nullable=True) # Storing tabular data as JSON for flexibility
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    engine = create_engine(Config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
