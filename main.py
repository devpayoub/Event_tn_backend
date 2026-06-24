from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from config import settings
from routes import auth, comments, events, meetings, posts, users

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect(host=settings.mongodb_uri)
    yield


app = FastAPI(
    title="Events API",
    version="1.0.0",
    docs_url="/api/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(meetings.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
