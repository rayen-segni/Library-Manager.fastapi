from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, models

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func

from ..databse import get_db
from ..oauth2 import get_current_user

from datetime import datetime
from dateutil import parser


router = APIRouter(
  prefix='/loans',
  tags=['Loans Mangement']
)

@router.post('/',
            response_model=schemas.LoanResponse, 
            status_code=status.HTTP_201_CREATED)
def add_book_loan(loan: schemas.LoanCreate,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(get_current_user)):
  
  #Authorization
    if current_user.role != "user":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="User privileges required")
    
  #verify cin existance
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    
    if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="Cin Not Found")
    
  #verify unique loan
    exist = db.query(models.Loan).filter(and_(models.Loan.book_id == loan.book_id,
                                      models.Loan.client_id == current_user.id,
                                      models.Loan.retrieved == False)).first()
    
    if exist is not None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Already loaned this book")
    
  #verify book copies & existance
    book_query = db.query(models.Book).filter(models.Book.id == loan.book_id)
    book = book_query.first()
    
    if book is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="Book Not Found")
    
    if book.copies < 1:
      min_date = (db.query(func.min(models.Loan.end_date))
                  .having(func.min(models.Loan.end_date) > func.now())
                  .scalar())
      
      #scalar returns a single python value
      #first return a row or tuple-like object it need unoacking to read
      
      #Tell how much days left
      if min_date:
        now = datetime.now(tz=min_date.tzinfo) # we have to add the time zone info to python allow us make comparisation
        days_left = (min_date - now).days
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Book will be availble in {days_left} days")
      
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Book is not available now")

  #verify on loan intervale
    
    now = datetime.now()
    end_date = loan.dict()["end_date"]
    
    days = (end_date - now).days
    
    if days < 1:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Duration must be at least 1 day")
    
    if days > 60:
      raise HTTPException(
          status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
          detail="Duration cannot exceed 60 days"
      )

    new_loan = models.Loan(client_id=current_user.id, **loan.dict())
    
    db.add(new_loan)
    
  #update book copies
    book.copies -= 1
    
    db.commit()
    db.refresh(new_loan)
  #return
    return new_loan


@router.get('/{id}',
            response_model=schemas.List[schemas.LoanResponse])
def get_book_user(id: int,
                  db: Session = Depends(get_db)):
  
  user = db.query(models.Loan).filter(models.Loan.client_id == id).all()
  
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User Not Found")
  
  return user


@router.post('/{title}')
def book_back(title: str,
              db: Session = Depends(get_db),
              current_user: schemas.TokenData = Depends(get_current_user)):
  
  #Authorization
  if current_user.role != "user":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="User privileges required")
  #verify on book name
  book = db.query(models.Book).filter(models.Book.title == title.lower()).first()
  
  if book is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book Not Found")
  
  #Verify on loan 
  loan = db.query(models.Loan).filter(and_(models.Loan.book_id == book.id, models.Loan.retrieved == False)).first()
  
  if loan is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Loan Not Found")

  #Save Return
  book.copies += 1
  loan.retrieved = True
  db.commit()
  
  #Alert
  now = datetime.now().date()
  default = parser.parse(str(loan.end_date)).date()
  #parse accept string and any format of date it always change it to => yyyy-mm-dd
  
  if default < now:
    return {"message": f"You made a delay of {(now - default).days} days"}

  return {"message": "Book Back With success"}


@router.get('/',
            response_model=schemas.List[schemas.LoanResponse])
def current_loans(db: Session = Depends(get_db),
                  current_user: schemas.TokenData = Depends(get_current_user)):
  
  if current_user.role != "admin":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Admin privileges required")
  
  current_loans = db.query(models.Loan).filter(models.Loan.retrieved == False)
  
  if current_loans is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No loans found now")
  
  return current_loans



