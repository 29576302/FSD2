from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import APIUser
from app.schemas.schemas import TokenBase
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["auth"])

# POST /token
@router.post("/token", response_model=TokenBase)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(APIUser).filter(APIUser.username == form_data.username).first()
    # Check if user exists
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Create access token
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

'''
Note: The brief asks us to implement a "/token endpoint where users can 
provide their username and password to obtain a JSON Web Token 
(JWT), which they will use to authenticate their requests to the other 
endpoints" for our POST, PUT, and DELETE endpoints. In the 'DELETE endpoints'
section, the brief refers to a JWT as a Java Web Token, which seems to be a
mistake. As per my interpretation, the brief is asking us to implement the
same function for all three endpoints.

I have implemented the POST /token endpoint as a login function, and the PUT
/token endpoint as a basic refresh token function. The DELETE /token endpoint
functions as described in the brief, but I have included an additional basic
logout function, which can be seen in the multiline comment below the DELETE endpoint.
'''

# PUT /token
@router.put("/token", response_model=TokenBase)
def refresh_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(form_data, db)

# DELETE /token
@router.delete("/token", response_model=TokenBase)
def delete_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(form_data, db)
'''
def logout():
    return {"message": "Logged out."}
'''
