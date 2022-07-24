import time

import uvicorn
from fastapi import FastAPI

from sqlalchemy.orm import Session

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


from database.config import SessionLocal, engine, Base
from database.models import Flower
from database.flowers import flower_list
from routers import photos, pictures

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(photos.router)
app.include_router(pictures.router)


# 분류용 꽃 세팅
@app.on_event("startup")
async def init():
    db: Session = SessionLocal()
    for flower in flower_list:
        if db.query(Flower).filter_by(kor_name=flower.kor_name).first() is None:
            db.add(flower)
            logger.info("분류용 꽃 데이터 세팅 = {}", flower.kor_name)
    db.commit()
    db.close()


# 미들웨어를 통한 통합 로깅 및 예외처리
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    logger.info("Request start")
    logger.info("headers = {}", request.headers)
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
async def welcome_page():
    return "Hello! this is a Flooming REST API Server."


if __name__ == "__main__":
    uvicorn.run(app)
