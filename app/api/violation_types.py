from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import ViolationType
from app.schemas.schemas import ViolationTypeResponse

# Violation Type API Router
router = APIRouter(
    prefix="/violation-types",
    tags=["Violation Types"]
)

# GET /violation-types
# Get all violation types
@router.get("/", response_model=List[ViolationTypeResponse])
def get_violation_types(db: Session = Depends(get_db)):
    violations = db.query(ViolationType).all()
    return violations