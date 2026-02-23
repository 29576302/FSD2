from fastapi import FastAPI, Request
from app.api import violation_types, drivers, correction_notices, auth, vehicles, notice_violations
from app.db.database import engine
from app.models import models
from app.core.security import hash_password
from app.db.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.responses import JSONResponse

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="NYSP Correction Notice API",
    description="RESTful API for NYSP Correction Notice System",
    version="1.0.0"
)

# Error handling
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=400, content={"detail": "Database integrity error"})

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"detail": "Internal database error"})

# Create sample accounts for testing
db = SessionLocal()
try:
    # If no users exist, create sample accounts
    if not db.query(models.APIUser).first():
        officer = models.APIUser(
            username="s_scott@localhost", 
            password=hash_password("password"), 
            role="officer"
        )
        citizen = models.APIUser(
            username="d_kroenke@localhost", 
            password=hash_password("password"), 
            role="citizen"
        )
        db.add(officer)
        db.add(citizen)
        db.commit()
finally:
    db.close()

# Include API routers
app.include_router(violation_types.router)
app.include_router(drivers.router)
app.include_router(correction_notices.router)
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(notice_violations.router)