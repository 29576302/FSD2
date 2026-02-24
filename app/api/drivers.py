from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Driver, CorrectionNotice, NoticeViolation
from app.schemas.schemas import DriverResponse, DriverCreate, DriverUpdate
from typing import List
from sqlalchemy import func
from app.core.deps import get_user_officer
from app.models.models import APIUser

# Driver API Router
router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

# GET /drivers/frequent-offenders
# Get drivers with more than a specified number of violations
@router.get("/frequent-offenders", response_model=List[DriverResponse])
def get_frequent_offenders(min_violations: int = 1, db: Session = Depends(get_db)):
    offenders = (
        db.query(Driver)
        .join(CorrectionNotice, Driver.driver_id == CorrectionNotice.driver_id)
        .join(NoticeViolation, CorrectionNotice.correction_notice_id == NoticeViolation.correction_notice_id)
        .group_by(Driver.driver_id)
        .having(func.count(NoticeViolation.notice_violation_id) > min_violations)
        .all()
    )
    return offenders

# GET /drivers/{driver_id}
# Get driver by ID
@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

# POST /drivers
# Create a new driver
# Only officers can create drivers
@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Check if driver with this licence already exists
    existing_driver = db.query(Driver).filter(Driver.drivers_licence == driver.drivers_licence).first()
    if existing_driver:
        raise HTTPException(status_code=409, detail="A driver with this licence already exists")
    new_driver = Driver(**driver.model_dump())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

# PUT /drivers/{driver_id}
# Update a driver
# Only officers can update drivers
@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver: DriverUpdate, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Find the driver to update
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    # If driver not found, raise 404 error
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    # Check if updating licence to one that already exists on another driver
    if driver.drivers_licence:
        existing_driver = db.query(Driver).filter(
            Driver.drivers_licence == driver.drivers_licence,
            Driver.driver_id != driver_id
        ).first()
        if existing_driver:
            raise HTTPException(status_code=409, detail="A driver with this licence already exists")
    # Update the driver
    update_data = driver.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_driver, key, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver