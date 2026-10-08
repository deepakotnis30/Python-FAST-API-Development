from fastapi import FastAPI
from fastapi import Depends
from app.routers import auth
from . import models
from .database import engine
import app.routers.post as post
import app.routers.user as user
import app.routers.vote as vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins =["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to My API Testing123!!!"}
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)