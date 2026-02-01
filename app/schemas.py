from pydantic import BaseModel, conint, constr, EmailStr, ConfigDict
from typing import Optional, Literal, List
from datetime import datetime, date

#Token

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int
  role: str


#User

class UserBase(BaseModel):
  cin: constr(max_length=8, min_length=8)
  role: Literal["admin", "user"] = "user"
  full_name: str
  email: EmailStr
  phone: constr(max_length=8, min_length=8)
  age: conint(gt=12)

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class UserResponse(UserBase):
  created_at: date
  id: int 
  
  model_config = ConfigDict(from_attributes=True)


#Book

class BookBase(BaseModel):
  title: str
  copies: int

class BookCreate(BookBase):
  pass

class BookUpdate(BaseModel):
  title: str
  action: Literal["increase", "reduce"]
  num: conint(gt=0)

class BookResponse(BookBase):
  added_at: datetime

class BookBack(BaseModel):
  cin: constr(max_length=8, min_length=8)

#Loan

class LoanBase(BaseModel):
  book_id: int
  days: int
  retrieved: bool = False

class LoanCreate(LoanBase):
  pass

class LoanResponse(LoanBase):
  start_date: datetime
  
  client: UserResponse
  book: BookResponse