from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import CorrectionNotice, Driver, Vehicle, Officer, APIUser
from app.schemas.schemas import CorrectionNoticeResponse, CorrectionNoticeCreate, CorrectionNoticeUpdate
from app.core.deps import get_user_officer

# Correction Notice API Router
router = APIRouter(
    prefix="/correction-notices",
    tags=["Correction Notices"]
)

# POST /correction-notices
# Create a new correction notice
# Only officers can create correction notices
@router.post("/", response_model=CorrectionNoticeResponse, status_code=201)
def create_correction_notice(correction_notice: CorrectionNoticeCreate, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Validate foreign keys exist
    if not db.query(Driver).filter(Driver.driver_id == correction_notice.driver_id).first():
        raise HTTPException(status_code=404, detail="Driver not found")
    if not db.query(Vehicle).filter(Vehicle.vehicle_id == correction_notice.vehicle_id).first():
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not db.query(Officer).filter(Officer.officer_id == correction_notice.officer_id).first():
        raise HTTPException(status_code=404, detail="Officer not found")
    new_correction_notice = CorrectionNotice(**correction_notice.model_dump())
    db.add(new_correction_notice)
    db.commit()
    db.refresh(new_correction_notice)
    return new_correction_notice

# PUT /correction-notices/{correction_notice_id}
# Update a correction notice
# Only officers can update correction notices
@router.put("/{correction_notice_id}", response_model=CorrectionNoticeResponse)
def update_correction_notice(correction_notice_id: int, correction_notice: CorrectionNoticeUpdate, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Find the correction notice to update
    db_correction_notice = db.query(CorrectionNotice).filter(CorrectionNotice.correction_notice_id == correction_notice_id).first()
    # If correction notice not found, raise 404 error
    if not db_correction_notice:
        raise HTTPException(status_code=404, detail="Correction notice not found")
    # Validate foreign keys if being updated
    if correction_notice.driver_id and not db.query(Driver).filter(Driver.driver_id == correction_notice.driver_id).first():
        raise HTTPException(status_code=404, detail="Driver not found")
    if correction_notice.vehicle_id and not db.query(Vehicle).filter(Vehicle.vehicle_id == correction_notice.vehicle_id).first():
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if correction_notice.officer_id and not db.query(Officer).filter(Officer.officer_id == correction_notice.officer_id).first():
        raise HTTPException(status_code=404, detail="Officer not found")
    # Update the correction notice
    update_data = correction_notice.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_correction_notice, key, value)
    db.commit()
    db.refresh(db_correction_notice)
    return db_correction_notice