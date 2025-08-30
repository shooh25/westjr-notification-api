from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.setting import router as setting_router
from app.services.notification import start_scheduler
from contextlib import asynccontextmanager

load_dotenv()

# サーバー起動時にスケジューラーを起動
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(setting_router)
