from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..databse import get_db
from .. import models, utils, schemas, oauth2


router = APIRouter(
  tags=['Authentication'])

@router.post('/login',
            response_model=schemas.Token)
def login(credentials : OAuth2PasswordRequestForm = Depends(),
          db : Session = Depends(get_db)):
  
  user_info = db.query(models.User).filter(models.User.cin == credentials.username).first()
  
  if not user_info :
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid crendentials")
  
  if not utils.verify(credentials.password, user_info.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid crendentials")
  
  access_token = oauth2.create_access_token(data={"user_id": user_info.id, "role": user_info.role})
  
  return {"access_token": access_token, "token_type": "Bearer"}

