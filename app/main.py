from fastapi import FastAPI
from .routers import auth, user, loan, books
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(loan.router)
app.include_router(books.router)

@app.get('/')
def main():
  return {"message": "Welcome to to the library manager"}
