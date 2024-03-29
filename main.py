import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from sqlalchemy.orm import Session

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.staticfiles import StaticFiles

from database.config import SessionLocal, engine, Base
from database.curd import set_represent_flowers, set_admin
from router import photo, picture, admin
from utils.config import secrets

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(photo.router)
app.include_router(picture.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


# 분류용 꽃 세팅
@app.on_event("startup")
def init():
    db: Session = SessionLocal()
    set_represent_flowers(db)
    set_admin(db, secrets["admin_password"])


# 미들웨어를 통한 통합 로깅 및 예외처리
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    logger.info("Request start")
    # logger.info("headers = {}", request.headers)
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info("Request Processing Time: {}s", round(process_time, 2))
        return response
    except Exception as e:
        logger.warning(f"Request failed: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        logger.info("Request end")


@app.get("/")
def welcome_page():
    return "Hello! this is a Flooming REST API Server."


if __name__ == "__main__":
    uvicorn.run(app)
