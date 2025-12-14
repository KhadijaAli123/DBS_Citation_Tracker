# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from sqlalchemy import or_, func

def create_citation(db: Session, citation_in: schemas.CitationCreate) -> models.Citation:
    db_cit = models.Citation(**citation_in.dict())
    db.add(db_cit)
    db.commit()
    db.refresh(db_cit)
    return db_cit

def get_citation(db: Session, citation_id: int) -> Optional[models.Citation]:
    return db.query(models.Citation).filter(models.Citation.id == citation_id).first()

def list_citations(db: Session, skip: int = 0, limit: int = 100, q: Optional[str] = None, sort_by: Optional[str] = None):
    query = db.query(models.Citation)
    if q:
        q_like = f"%{q}%"
        query = query.filter(or_(models.Citation.title.ilike(q_like),
                                 models.Citation.authors.ilike(q_like),
                                 models.Citation.tags.ilike(q_like),
                                 models.Citation.venue.ilike(q_like)))
    if sort_by == "year":
        query = query.order_by(models.Citation.year.desc())
    else:
        query = query.order_by(models.Citation.created_at.desc())
    return query.offset(skip).limit(limit).all()

def update_citation(db: Session, citation_id: int, citation_in: schemas.CitationUpdate):
    db_cit = get_citation(db, citation_id)
    if not db_cit:
        return None
    for field, value in citation_in.dict(exclude_unset=True).items():
        setattr(db_cit, field, value)
    db.add(db_cit)
    db.commit()
    db.refresh(db_cit)
    return db_cit

def delete_citation(db: Session, citation_id: int) -> bool:
    db_cit = get_citation(db, citation_id)
    if not db_cit:
        return False
    db.delete(db_cit)
    db.commit()
    return True

# reporting helpers
def report_top_authors(db: Session, limit: int = 10):
    # naive split-by-comma aggregation; for robust solution you'd normalize authors to separate table
    # This function returns top author strings by count
    authors_data = db.query(models.Citation.authors, func.count(models.Citation.id)).group_by(models.Citation.authors).order_by(func.count(models.Citation.id).desc()).limit(limit).all()
    return [{"authors": a, "count": c} for a, c in authors_data]

def total_count(db: Session):
    return db.query(func.count(models.Citation.id)).scalar()

