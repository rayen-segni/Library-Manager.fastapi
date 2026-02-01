from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes

def create_access_token(data: dict):
  
  to_encode = data.copy()
  
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
  
  to_encode.update({"exp": expire})
  
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return token

def verify_access_token(token: str, credentials_exeption):
  
  try:
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    id = payload.get('user_id')
    role = payload.get('role')
    
    if id is None or role is None:
      raise credentials_exeption

    token_data = schemas.TokenData(id=id, role=role)
    
  except JWTError:
    raise credentials_exeption

  return token_data

def get_current_user(token: str = Depends(oauth2_schema)):
  
  credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could Not Validate Credentials",
                                      headers={"WWW-Authenticate": "Bearer"})
  
  return verify_access_token(token, credentials_exeption)

