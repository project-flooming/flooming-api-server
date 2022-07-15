import os
import uuid

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from ai.inference import classify
from database.config import get_db
from database.models import Photo, Flower

from loguru import logger

router = APIRouter()


async def check_anomaly(classify_result):
    prob = [result["probability"] for result in classify_result]
    gap1 = abs(prob[0] - prob[1])
    gap2 = abs(prob[1] - prob[2])
    gap3 = abs(prob[0] - prob[2])
    if gap1 <= 1 and gap2 <= 1 and gap3 <= 1:
        raise HTTPException(status_code=400, detail="업로드한 사진이 꽃이 아닙니다.")


async def make_response_list(classify_result, db):
    result_response = []
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
    return result_response


async def upload(file):
    try:
        UPLOAD_DIR = "./photo"
        content = await file.read()
        logger.info(f"original filename = {file.filename}")
        filename = f"{str(uuid.uuid4())}.jpg"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(content)
        src = f"{UPLOAD_DIR}/{filename}"
        return filename, src
    except Exception:
        raise HTTPException(status_code=400, detail="꽃 사진 업로드 오류")


# 사진 업로드 후 꽃 분류
@router.post("/photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    # 서버 로컬 스토리지에 이미지 저장
    filename, src = await upload(file)

    # 디비에 저장
    db_photo = Photo(filename=filename, src=src)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    # 꽃 분류
    classify_result = await classify(src)

    # 잘못된 사진 거르기
    await check_anomaly(classify_result)

    logger.info("분류 결과 = {}", classify_result)

    return {"result": await make_response_list(classify_result, db), "photo_id": db_photo.photo_id}


# 사진 다운로드
@router.get("/download/photo/{photo_id}")
async def download_photo(photo_id: int, db: Session = Depends(get_db)):
    find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
    if find_photo is None:
        raise HTTPException(status_code=400, detail="사진 다운로드 실패 : 해당 사진을 찾을 수 없습니다.")
    return FileResponse(find_photo.src)