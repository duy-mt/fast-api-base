from fastapi import FastAPI
from app.routers import user, session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
