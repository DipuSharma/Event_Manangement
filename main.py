import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.configuration.settings import setting
from src.app.event import router as event_router
from src.app.auth import router as auth_router
from src.app.attendee import router as attendee_router
from src.configuration.db_setting import init_db
from src.worker.celery_worker import celery_app


app = FastAPI(
    title=setting.TITLE,
    docs_url="/event" if setting.DEBUG else None,
    debug=setting.DEBUG,
)

origins = ["0.0.0.0"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    init_db()


app.mount("/static", StaticFiles(directory="static"), name="static")
# app.include_router(auth_router.router)
# app.include_router(super_admin.router)
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(event_router.router, prefix="/events", tags=["Events"])
app.include_router(attendee_router.router, prefix="/attendee", tags=["Attendee"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(setting.HOST_PORT), reload=True)
