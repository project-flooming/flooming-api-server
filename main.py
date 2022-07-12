import os.path

import uvicorn
from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.responses import FileResponse

from database.config import SessionLocal, engine, Base
from database.models import Picture, Photo, Flower
import uuid
import logging
from ai.inference import classify
from database.flowers import flower_list

# 데이터베이스 스키마 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    try:
        return await call_next(request)
    except Exception as e:
        logger.warning(f"Request failed: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        logger.info("Request end")


# 사진 업로드 후 꽃 분류
@app.post("/photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    # 서버 로컬 스토리지에 이미지 저장
    UPLOAD_DIR = "./photo"

    content = await file.read()
    logging.info(f"original filename = {file.filename}")
    filename = f"{str(uuid.uuid4())}.jpg"
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)
    src = f"{UPLOAD_DIR}/{filename}"

    # 디비에 저장
    db_photo = Photo(filename=filename, src=src)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    # 꽃 분류
    result_response = []
    classify_result = classify(src)

    prob = [result["probability"] for result in classify_result]
    gap1 = abs(prob[0] - prob[1])
    gap2 = abs(prob[1] - prob[2])
    gap3 = abs(prob[0] - prob[2])
    if gap1 <= 1 and gap2 <= 1 and gap3 <= 1:
        return {"result": "anomaly"}

    logger.info("분류 결과 = {}", classify_result)
    for result in classify_result:
        flower: Flower = db.query(Flower).filter_by(kor_name=result["type"]).first()
        if flower is None:
            continue
        data = {
            "probability": result["probability"],
            "kor_name": flower.kor_name,
            "eng_name": flower.eng_name,
            "flower_language": flower.flower_language,
            "img_src": flower.img_src
        }
        result_response.append(data)

    return {"result": result_response}


# 사진 타입 변경 (사용자가 사진 최종 선택)
@app.put("/photo/{photo_id}/{flower_type}")
async def update_photo_type(photo_id: int, flower_type: str, db: Session = Depends(get_db)):
    db.query(Photo).filter_by(photo_id=photo_id).update({"type": flower_type})
    db.commit()
    return db.query(Photo).filter_by(photo_id=photo_id).first()


# 사진 가져오기
@app.get("/photo/{photo_id}")
async def get_photo_by_id(photo_id, db: Session = Depends(get_db)):
    return db.query(Photo).filter_by(photo_id=photo_id).first()


# 사진 -> 그림 변환
@app.post("/picture/{photo_id}")
async def create_picture(photo_id: int):
    # 그림 변환
    return True


# 사진 다운로드
@app.get("/download/photo/{photo_id}")
async def download_photo(photo_id: int, db: Session = Depends(get_db)):
    find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
    return FileResponse(find_photo.src)


# 그림 다운로드
@app.get("/download/picture")
async def download_picture():
    return True


# 갤러리 - 사진/그림 업로드
@app.post("/gallery")
async def create_gallery(db: Session = Depends(get_db)):
    return True


# 갤러리 - 사진/그림 리스트 반환
@app.get("/gallery")
async def get_all_gallery(db: Session = Depends(get_db)):
    result = db.query(Picture).all()
    return result


@app.get("/")
async def welcome_page():
    return "안녕하세요. Flooming REST API 서버입니다."


if __name__ == "__main__":
    uvicorn.run(app)
