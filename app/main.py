import os.path

import uvicorn
from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine
from app import models
from app.models import Picture, Photo
from app.schemas import RequestPhoto, ResponsePicture
import uuid

# 데이터베이스 스키마 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"안녕하세요": "꽃분이 입니다."}


# 사진 업로드
@app.post("/photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    UPLOAD_DIR = "C:\dev"

    content = await file.read()
    filename = f"{str(uuid.uuid4())}.png"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)
    src = f"{UPLOAD_DIR}/{filename}"

    # 꽃 사진
    return {"filename": filename, "src": src}


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
@app.get("/gallery", response_model=List[ResponsePicture])
async def get_all_gallery(db: Session = Depends(get_db)):
    result = db.query(Picture).all()
    return result


@app.get("/test")
async def test():
    print("요청이 와써용")
    return {"테스트": "입니다"}


if __name__ == "__main__":
    uvicorn.run(app)
