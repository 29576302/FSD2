# This is a RESTful API for the New York State Patrol Correction Notice System, built with Python and FastAPI.

# Requirements
Python 3.12.0 is REQUIRED for this program.

# How to run:
1. Create a virtual environment using
`python -m venv venv`
2. Install dependencies using
`pip install -r requirements.txt`
3. Run Docker container.
4. Create the database by running `NYSP_Corrections_DB.sql` in MySQL Workbench
5. Start the FastAPI server using
`uvicorn app.main:app --reload`
6. When testing JWTs and JWT restricted endpoints, use the sample officer account.

# Sample accounts:
| Role    | Username            | Password |
|---------|---------------------|----------|
| Citizen | d_kroenke@localhost | password |
| Officer | s_scott@localhost   | password |

# Project structure:
```
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── correction_notices.py
│   │   ├── drivers.py
│   │   ├── notice_violations.py
│   │   ├── vehicles.py
│   │   └── violation_types.py
│   │
│   ├── core/
│   │   ├── deps.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── models.py
│   │
│   └── schemas/
│       └── schemas.py
│
├── NYSP_Corrections_DB.sql
├── README.md
└── requirements.txt
```
