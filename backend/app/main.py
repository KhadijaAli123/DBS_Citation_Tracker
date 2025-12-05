# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from . import models, schemas, crud
from .database import engine, Base
from .deps import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DBS Academic Citation Tracker API")

@app.post("/api/citations/", response_model=schemas.CitationOut)
def create_citation(citation_in: schemas.CitationCreate, db: Session = Depends(get_db)):
    # check DOI uniqueness if provided
    if citation_in.doi:
        existing = db.query(models.Citation).filter(models.Citation.doi == citation_in.doi).first()
        if existing:
            raise HTTPException(status_code=400, detail="Citation with this DOI already exists")
    return crud.create_citation(db, citation_in)

@app.get("/api/citations/{citation_id}", response_model=schemas.CitationOut)
def read_citation(citation_id: int, db: Session = Depends(get_db)):
    cit = crud.get_citation(db, citation_id)
    if not cit:
        raise HTTPException(status_code=404, detail="Citation not found")
    return cit

@app.get("/api/citations/", response_model=List[schemas.CitationOut])
def list_citations(skip: int = 0, limit: int = 100, q: Optional[str] = Query(None), sort_by: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return crud.list_citations(db, skip=skip, limit=limit, q=q, sort_by=sort_by)

@app.put("/api/citations/{citation_id}", response_model=schemas.CitationOut)
def update_citation(citation_id: int, citation_in: schemas.CitationUpdate, db: Session = Depends(get_db)):
    updated = crud.update_citation(db, citation_id, citation_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Citation not found")
    return updated

@app.delete("/api/citations/{citation_id}")
def delete_citation(citation_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_citation(db, citation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Citation not found")
    return {"deleted": True}

# Reporting endpoints
@app.get("/api/report/summary")
def report_summary(db: Session = Depends(get_db)):
    return {"total_citations": crud.total_count(db)}

@app.get("/api/report/top_authors")
def report_top_authors(limit: int = 10, db: Session = Depends(get_db)):
    return {"top_authors": crud.report_top_authors(db, limit=limit)}
