from fastapi import FastAPI
from app.routers import user, session
from fastapi.middleware.cors import CORSMiddleware
from app.jobs.scheduler import start_scheduler
from app.config.index import settings

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("Scheduler started.")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
