from fastapi import FastAPI
from .routers import auth, user, loan, books

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(loan.router)
app.include_router(books.router)
