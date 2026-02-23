from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import NoticeViolation, APIUser
from app.core.deps import get_user_officer

# Notice Violation API Router
router = APIRouter(
    prefix="/notice-violations",
    tags=["Violations Within a Correction Notice"]
)

# DELETE /notice-violations/{notice_violation_id}
# Delete a notice violation
# Only officers can delete notice violations
@router.delete("/{notice_violation_id}")
def delete_violation(notice_violation_id: int, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Find the notice violation to delete
    db_notice_violation = db.query(NoticeViolation).filter(NoticeViolation.notice_violation_id == notice_violation_id).first()
    # If notice violation not found, raise 404 error
    if not db_notice_violation:
        raise HTTPException(status_code=404, detail="Notice violation not found")
    # Delete the notice violation
    db.delete(db_notice_violation)
    db.commit()
    return {"message": f"Notice violation {notice_violation_id} deleted successfully"}