from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session 
from ..database import get_db
from ..schemas import UserLogin
from .. import models, utils, oauth2, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    
    if not utils.verify_password(user_credential.password, user.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer"}
    

    
