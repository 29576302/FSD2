from os import getenv
from datetime import timedelta, datetime
from jose import jwt
from passlib.context import CryptContext

# Security configuration
SECRET_KEY = getenv("SECRET_KEY", "1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Passlib for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to create access token
# Generates a JWT token valid for 30 minutes
def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)