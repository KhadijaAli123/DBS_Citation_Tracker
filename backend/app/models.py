# models.py
from sqlalchemy import Column, Integer, String, Text, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class Citation(Base):
    __tablename__ = "citations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(400), nullable=False, index=True)
    authors = Column(String(400), nullable=False)  # comma-separated for simplicity
    venue = Column(String(200), nullable=True)
    year = Column(Integer, nullable=True)
    doi = Column(String(200), nullable=True, unique=True)
    tags = Column(String(200), nullable=True)  # comma-separated tags
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
