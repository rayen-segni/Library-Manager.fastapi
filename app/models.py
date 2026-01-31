from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .databse import Base

class Book(Base):
  __tablename__ = 'books'
  
  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, unique=True, nullable=False)
  copies = Column(Integer, server_default='0', nullable=False)
  added_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True, nullable=False)
  cin = Column(String, unique=True, nullable=False)
  role = Column(String, server_default='user', nullable=False)
  full_name = Column(String, nullable=False)
  email = Column(String, unique=True, nullable=False)
  phone = Column(Integer, unique=True, nullable=True)
  age = Column(Integer, nullable=False)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

class Loan(Base):
  __tablename__ = 'loans'
  
  id = Column(Integer, primary_key=True, nullable=False)
  client_id = Column(Integer,  ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
  book_id = Column(Integer, ForeignKey(Book.id, ondelete='CASCADE'), nullable=False)
  start_date = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
  end_date = Column(TIMESTAMP(timezone=True), nullable=False)
  retrieved = Column(Boolean, server_default='FALSE', nullable=False)

  client = relationship("User")
  book = relationship("Book")


