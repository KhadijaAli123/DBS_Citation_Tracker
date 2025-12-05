# test_crud.py
import pytest
from app import models, schemas, crud
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import os

@pytest.fixture(scope="module")
def db():
    # create a fresh in-memory SQLite for tests, or use temporary file
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine_test = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_and_get(db: Session):
    c_in = schemas.CitationCreate(title="Test Paper", authors="Alice, Bob", venue="J Test", year=2020)
    created = crud.create_citation(db, c_in)
    assert created.id is not None
    fetched = crud.get_citation(db, created.id)
    assert fetched.title == "Test Paper"

def test_update(db: Session):
    c_in = schemas.CitationCreate(title="To Update", authors="X", year=2019)
    created = crud.create_citation(db, c_in)
    updated = crud.update_citation(db, created.id, schemas.CitationUpdate(title="Updated Title"))
    assert updated.title == "Updated Title"

def test_delete(db: Session):
    c_in = schemas.CitationCreate(title="To Delete", authors="Z")
    created = crud.create_citation(db, c_in)
    ok = crud.delete_citation(db, created.id)
    assert ok
    assert crud.get_citation(db, created.id) is None
