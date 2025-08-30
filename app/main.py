from fastapi import FastAPI, Request, HTTPException
import httpx
import os
from dotenv import load_dotenv
from app.api.setting import router as setting_router

load_dotenv()
app = FastAPI()
app.include_router(setting_router)