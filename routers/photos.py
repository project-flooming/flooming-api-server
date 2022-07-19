import datetime
import os
import random
import uuid

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from ai.inference import classify
from database.config import get_db
from database.models import Photo, Flower

from loguru import logger

router = APIRouter()


async def validate(classify_result, src):
    prob_list = [result["probability"] for result in classify_result]
    max_prob = max(prob_list)
    if max_prob >= 95:
        return classify_result[0]
    elif max_prob <= 75:
        await delete_photo(src)
        raise HTTPException(status_code=400, detail="알아볼 수 없는 사진이에요. 다시 사진을 올려주세요.")


# def make_response_list(classify_result, db):
#     result_response = []
#     for result in classify_result:
#         flower: Flower = db.query(Flower).filter_by(kor_name=result["type"]).first()
#         if flower is None:
#             continue
#         data = {
#             "probability": result["probability"],
#             "kor_name": flower.kor_name,
#             "eng_name": flower.eng_name,
#             "flower_language": flower.flower_language,
#             "img_src": flower.img_src
#         }
#         result_response.append(data)
#     return result_response

def make_response(classify_result, db):
    print(classify_result)
    flower: Flower = db.query(Flower).filter_by(kor_name=classify_result[0]["type"]).first()
    return {
        "probability": classify_result[0]["probability"],
        "kor_name": flower.kor_name,
        "eng_name": flower.eng_name,
        "flower_language": flower.flower_language,
        "img_src": flower.img_src
    }


async def upload(file):
    try:
        UPLOAD_DIR = "./photo"
        content = await file.read()
        logger.info(f"original filename = {file.filename}")
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{random.randint(0, 1000)}.jpg"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(content)
        src = f"{UPLOAD_DIR}/{filename}"
        return filename, src
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=400, detail="꽃 사진 업로드 오류")


async def delete_photo(src):
    os.remove(src)


# 사진 업로드 후 꽃 분류
@router.post("/photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    # 서버 로컬 스토리지에 이미지 저장
    filename, src = await upload(file)

    # 꽃 분류
    classify_result = classify(src)
    logger.info("Classify Result = {}", classify_result)

    # 잘못된 사진 거르기
    result = await validate(classify_result, src)

    # 디비에 저장
    db_photo = Photo(filename=filename, src=src)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    # return {"result": make_response_list(result, db), "photo_id": db_photo.photo_id}
    flower: Flower = db.query(Flower).filter_by(kor_name=classify_result[0]["type"]).first()

    return {
        "photo_id": db_photo.photo_id,
        "probability": result["probability"],
        "kor_name": flower.kor_name,
        "eng_name": flower.eng_name,
        "flower_language": flower.flower_language,
        "img_src": flower.img_src
    }


# 사진 다운로드
@router.get("/download/photo/{photo_id}")
async def download_photo(photo_id: int, db: Session = Depends(get_db)):
    find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
    if find_photo is None:
        raise HTTPException(status_code=400, detail="사진 다운로드 실패 : 해당 사진을 찾을 수 없습니다.")
    return FileResponse(find_photo.src)