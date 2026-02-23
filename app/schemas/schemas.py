from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional, Literal

### Reference use of Field() for validation and description
### https://docs.pydantic.dev/latest/concepts/fields/#inspecting-model-fields
### Reference use of Literal and Optional for type safety and proper error handling
### https://docs.pydantic.dev/1.10/usage/types/

'''
Driver Schemas
'''
# Base driver schema
class DriverBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., min_length=2, max_length=2, description="2-letter state abbreviation (e.g., 'NY')")
    zip_code: str = Field(..., max_length=10)
    drivers_licence: str = Field(..., max_length=19)
    drivers_licence_state: str = Field(..., min_length=2, max_length=2, description="2-letter state abbreviation (e.g., 'NY')")
    birth_date: date
    height: int
    weight: int
    eyes: str = Field(..., max_length=20)

# Create driver schema
class DriverCreate(DriverBase):
    pass

# Update driver schema
# Optional fields, so specific fields can be updated
class DriverUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="2-letter state abbreviation (e.g., 'NY')")
    zip_code: Optional[str] = Field(None, max_length=10)
    drivers_licence: Optional[str] = Field(None, max_length=19)
    drivers_licence_state: Optional[str] = Field(None, min_length=2, max_length=2, description="2-letter state abbreviation (e.g., 'NY')")
    birth_date: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    eyes: Optional[str] = Field(None, max_length=20)

# Response driver schema
class DriverResponse(DriverBase):
    driver_id: int

    class Config:
        orm_mode = True

'''
Correction Notice Schemas
'''
# Base correction notice schema
# Booleans are defaulted to False
class CorrectionNoticeBase(BaseModel):
    driver_id: int
    vehicle_id: int
    officer_id: int
    violation_date: date
    violation_time: time
    location: str = Field(..., max_length=255)
    district: str = Field(..., max_length=100)
    warning: bool = False
    repair_vehicle: bool = False
    correct_immediately: bool = False

# Create correction notice schema
class CorrectionNoticeCreate(CorrectionNoticeBase):
    pass

# Update correction notice schema
# Optional fields, so specific fields can be updated
class CorrectionNoticeUpdate(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    officer_id: Optional[int] = None
    violation_date: Optional[date] = None
    violation_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=100)
    warning: Optional[bool] = None
    repair_vehicle: Optional[bool] = None
    correct_immediately: Optional[bool] = None

# Response correction notice schema
class CorrectionNoticeResponse(CorrectionNoticeBase):
    correction_notice_id: int

    class Config:
        orm_mode = True

'''
Violation Type Schemas
'''
# Base violation type schema
class ViolationTypeBase(BaseModel):
    description: str = Field(..., max_length=255)
    violation_code: str = Field(..., max_length=20)

# Response violation type schema
class ViolationTypeResponse(ViolationTypeBase):
    violation_type_id: int
    description: str
    violation_code: str

    class Config:
        orm_mode = True

'''
Token and API User Schemas
'''
# Token schema used for JWT authentication
# Token type is set to "bearer" by default
class TokenBase(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Token data schema used for JWT authentication
# Optional fields to allow for proper error handling
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None 

# Create user schema
# Sensible character limits for username and password
# Role must be either "officer" or "citizen"
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)
    role: Literal["officer", "citizen"]

# Response user schema
class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str

    class Config:
        orm_mode = True

