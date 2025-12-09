Project Overview:
The DBS Academic Citation Tracker is an information system developed to help students and academic staff organise, manage, and track academic citations. The prototype demonstrates core CRUD functionality and API-driven operations using FastAPI for the backend and HTML/CSS/JavaScript for the frontend.

Key Features:
- Create new citations
- Read and list all citations
- Update existing citation details
- Delete unwanted citations
- Search functionality across multiple fields
- Summary reporting
- REST API communication using fetch()
- SQLite database with SQLAlchemy ORM

System Architecture:
Frontend: HTML, CSS, JavaScript (fetch API)
Backend: Python FastAPI, Pydantic validation
Database: SQLite with SQLAlchemy ORM
Design: API-based, no page refresh, dynamic DOM updates

Project Structure:
backend/
  - main.py
  - models.py
  - schemas.py
  - database.py
  - tests/
frontend/
  - index.html
  - style.css
  - app.js

How to Run:
1. Install dependencies:
   pip install -r requirements.txt
2. Start backend server:
   uvicorn backend.main:app --reload
3. Open frontend:
   frontend/index.html (no server needed)

Testing:
- Unit tests for CRUD logic
- Integration test using FastAPI TestClient
Run tests with:
   pytest

Future Enhancements:
- Export citations to BibTeX / APA / Harvard
- User login & authentication
- Cloud deployment
- Pagination and filtering
- Automated DOI lookup

Author: Khadija Ali.
Student Name: Khadija Ali.
Student ID: 20071069.
Dublin Business School.
Module: Programming for information system.
