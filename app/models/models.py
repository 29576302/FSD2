from sqlalchemy import Column, Integer, String, Date, Time, Boolean, SmallInteger, ForeignKey
from app.db.database import Base

'''
Models for the database
Mostly based on the NYSP_Corrections_DB.sql file
'''

# Driver Model
class Driver(Base):
    __tablename__ = "driver"
    driver_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    drivers_licence = Column(String(19), nullable=False)
    drivers_licence_state = Column(String(2), nullable=False)
    birth_date = Column(Date, nullable=False)
    height = Column(SmallInteger, nullable=False)
    weight = Column(SmallInteger, nullable=False)
    eyes = Column(String(20), nullable=False)

# Officer Model
class Officer(Base):
    __tablename__ = "officer"
    officer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    personell_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    detachment = Column(String(100), nullable=False)

# Vehicle Owner Model
class VehicleOwner(Base):
    __tablename__ = "vehicle_owner"
    vehicle_owner_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_name = Column(String(255), nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)

# Violation Type Model
class ViolationType(Base):
    __tablename__ = "violation_type"
    violation_type_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), unique=True, nullable=False)
    violation_code = Column(String(20), nullable=False)

# Vehicle Model
class Vehicle(Base):
    __tablename__ = "vehicle"
    vehicle_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_owner_id = Column(Integer, ForeignKey("vehicle_owner.vehicle_owner_id"), nullable=False)
    vehicles_licence = Column(String(20), nullable=False)
    state = Column(String(2), nullable=False)
    colour = Column(String(30), nullable=False)
    make = Column(String(50), nullable=False)
    vin = Column(String(17), unique=True, nullable=False)
    year = Column(SmallInteger, nullable=False)
    type = Column(String(50), nullable=False)

# Correction Notice Model
class CorrectionNotice(Base):
    __tablename__ = "correction_notice"
    correction_notice_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_id = Column(Integer, ForeignKey("driver.driver_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"), nullable=False)
    officer_id = Column(Integer, ForeignKey("officer.officer_id"), nullable=False)
    violation_date = Column(Date, nullable=False)
    violation_time = Column(Time, nullable=False)
    location = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    warning = Column(Boolean, default=False, nullable=False)
    repair_vehicle = Column(Boolean, default=False, nullable=False)
    correct_immediately = Column(Boolean, default=False, nullable=False)

# Notice Violation Model
class NoticeViolation(Base):
    __tablename__ = "notice_violation"
    notice_violation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correction_notice_id = Column(Integer, ForeignKey("correction_notice.correction_notice_id"), nullable=False)
    violation_type_id = Column(Integer, ForeignKey("violation_type.violation_type_id"), nullable=False)

# API User Model
# New model for JWT authentication and role-based access control
class APIUser(Base):
    __tablename__ = "api_user"
    api_user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # "officer" or "citizen" - validated in schema