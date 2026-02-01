from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from ..databse import get_db

router = APIRouter(
  prefix="/books",
  tags=["Library Management"]
)

#show books
@router.get('/')
def show_books(db: Session = Depends(get_db),
              response_model=schemas.List[schemas.BookResponse],
              current_user: schemas.TokenData = Depends(oauth2.get_current_user),
              limit: int = 5, search:str = ""):
  
  books = (db.query(models.Book)
          .filter(models.Book.title.contains(search.lower()))
          .limit(limit)
          .all())
  
  if books is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No Books Found")
  
  return books

#Add book
@router.post('/',
            response_model=schemas.BookResponse,
            status_code=status.HTTP_201_CREATED)
def add_book(book: schemas.BookCreate,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  if current_user.role != "admin":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Admin privilges required")
  
  book_dict = book.dict()
  book_dict["title"] = book_dict["title"].lower()
  
  new_book = models.Book(**book_dict)
  
  try:
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Book already exist")
  
  return new_book

#Delete book
@router.delete('/{title}',
              status_code=status.HTTP_204_NO_CONTENT)
def delete_book(title: str,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  if current_user.role != "admin":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Admin privilges required")
  
  book = db.query(models.Book).filter(models.Book.title == title)
  
  if book.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book Not Found")
  
  #verify that the book not loaned
  exist = db.query(models.Loan).filter(and_(models.Loan.book_id == book.first().id, models.Loan.retrieved == False)).first
  
  if exist is not None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Book is loaned")
  
  book.delete(synchronize_session=False)
  db.commit()
  
  return status.HTTP_204_NO_CONTENT

#Update book copies
@router.put('/',
            response_model=schemas.BookResponse)
def update_book_copies(book: schemas.BookUpdate,
                      db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  if current_user.role != "admin":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Admin privileges required")
  
  old_book = db.query(models.Book).filter(models.Book.title == book.title).first()
  
  if book.action == "increase":
    old_book.copies += book.num
  else:
    if old_book.copies - book.num < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f"It left only {old_book.copies} books in the library")
    
    old_book.copies -= book.num
  
  db.commit()
  
  return old_book


