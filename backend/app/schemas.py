# schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class CitationBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=400)
    authors: str = Field(..., min_length=1, max_length=400)  # could be list but we keep string for simple UI
    venue: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None

    @validator("year")
    def check_year(cls, v):
        if v is not None and (v < 1700 or v > 2100):
            raise ValueError("year must be between 1700 and 2100")
        return v

class CitationCreate(CitationBase):
    pass

class CitationUpdate(BaseModel):
    title: Optional[str]
    authors: Optional[str]
    venue: Optional[str]
    year: Optional[int]
    doi: Optional[str]
    tags: Optional[str]
    notes: Optional[str]

class CitationOut(CitationBase):
    id: int

    class Config:
        orm_mode = True
