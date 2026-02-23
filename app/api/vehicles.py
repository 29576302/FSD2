from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Vehicle, APIUser
from app.core.deps import get_user_officer

# Vehicle API Router
router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

# DELETE /vehicles/{vehicle_id}
# Delete a vehicle from the database
# Only officers can delete vehicles
@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user: APIUser = Depends(get_user_officer)):
    # Find the vehicle to delete
    db_vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    # If vehicle not found, raise 404 error
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    # Delete the vehicle
    db.delete(db_vehicle)
    db.commit()
    return {"message": f"Vehicle {vehicle_id} deleted successfully"}