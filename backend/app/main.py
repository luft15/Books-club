# # backend/app/main.py

###################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_router, book_club_router

app = FastAPI(title="Book Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(book_club_router)

@app.get("/")
def root():
    return {
        "message": "Book Club API",
        "frontend": "http://localhost:3000",
        "backend": "http://localhost:8000"
        }
