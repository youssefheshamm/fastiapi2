from fastapi import FastAPI
from app.routers import tasks, utils
from app.database import engine, Base
import os
from dotenv import load_dotenv

load_dotenv()

BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD_HASH = os.getenv("BASIC_AUTH_PASSWORD_HASH")

app = FastAPI()

app.include_router(tasks.router)
app.include_router(utils.router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
