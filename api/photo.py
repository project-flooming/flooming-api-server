
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from deep_learning.inference import classify
from database.config import get_db
from database.models import Photo, Flower

from loguru import logger

from database.curd import get_represent_flower, save, find
from service.photo import upload, validate

router = APIRouter()


# 사진 업로드 후 꽃 분류
@router.post("/photo")
def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    # 서버 로컬 스토리지에 이미지 저장
    filename, src = upload(file)

    # 꽃 분류
    classify_result = classify(src)
    logger.info("Classify Result = {}", classify_result)

    # 잘못된 사진 거르기
    result = validate(classify_result, src)

    # 디비에 저장
    flower: Flower = get_represent_flower(db, classify_result[0]["type"])

    saved_photo = save(db, Photo(filename=filename, saved_path=src, flower_type=flower.kor_name))

    return {
        "photo_id": saved_photo.photo_id,
        "probability": result["probability"],
        "kor_name": flower.kor_name,
        "eng_name": flower.eng_name,
        "flower_language": flower.flower_language
    }


# 대표 사진 조회
@router.get("/flower/{filename}")
def get_basic_flower_img(filename: str):
    BASIC_FLOWER_URL = f"./image/photo/{filename}.jpg"
    return FileResponse(BASIC_FLOWER_URL)


# 사진 조회 및 다운로드
@router.get("/photo/{photo_id}")
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    return FileResponse(find(db, Photo, photo_id).saved_path)