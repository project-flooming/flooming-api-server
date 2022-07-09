import os.path
from datetime import datetime

import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger

import uuid
from app.database import dynamo_db

app = FastAPI()


# 미들웨어를 통한 통합 로깅 및 예외처리
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    logger.info("Request start")
    try:
        return await call_next(request)
    except Exception as e:
        logger.warning(f"Request failed: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        logger.info("Request end")


# 사진 업로드
@app.post("/photo")
async def upload_photo(file: UploadFile):
    # 서버 로컬 스토리지에 이미지 저장
    UPLOAD_DIR = "./photo"

    content = await file.read()
    logger.info(f"original filename = {file.filename}")
    filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)
    src = f"{UPLOAD_DIR}/{filename}"

    # 디비에 저장
    data = {"filename": filename, "src": src, "created_time": str(datetime.now())}
    dynamo_db().put_item(Item=data)
    return data


# 사진 가져오기
@app.get("/photo/{filename}")
async def get_photo(filename: str):
    return dynamo_db().get_item(Key={"filename": filename})["Item"]


# 사진 -> 그림 변환
@app.get("/picture/{filename}")
async def create_picture(filename):
    # 그림 변환
    return True


# 사진 다운로드
@app.get("/download/photo")
async def download_photo():
    return True


# 그림 다운로드
@app.get("/download/picture")
async def download_picture():
    return True


# 갤러리 - 사진/그림 리스트 반환
@app.get("/gallery")
async def get_all_gallery():
    return True


if __name__ == "__main__":
    uvicorn.run(app)
