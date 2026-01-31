from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, utils, oauth2, models
from ..databse import get_db



router = APIRouter(
  prefix='/users',
  tags=['Users Managemnt']
)

#Get Users
@router.get('/',
          response_model=schemas.List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db),
                  current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  if current_user.role != "admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Admin privileges required")
  
  users = db.query(models.User).all()
  
  if users is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No Users Found")

  return users

#Get User
@router.get('/{id}',
          response_model=schemas.UserResponse)
def get_user(id: int,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  user = db.query(models.User).filter(models.User.id == id).first()
  
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found")
  
  return user



#Add User
@router.post('/',
            response_model=schemas.UserResponse,
            status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.UserCreate,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  

  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  
  new_user = models.User(**user.dict())
  
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="User already exist")
    
  return new_user

#Delete User
@router.delete('/{id}', 
              status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

  user = db.query(models.User).filter(models.User.id == id)
  
  if user.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found")
  
  user.delete(synchronize_session=False)
  db.commit()
  
  return status.HTTP_204_NO_CONTENT

#Update User
@router.put('/{id}',
            response_model=schemas.UserResponse)
def update_user(id: int,
                user: schemas.UserCreate,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  user_query = db.query(models.User).filter(models.User.id == id)
  
  if user_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found")
    
  user_dict = user.dict()
  user_dict["password"] = utils.hash(user_dict["password"])
  
  user_query.update(user_dict, synchronize_session=False)
  db.commit()
  
  return user_query.first()

