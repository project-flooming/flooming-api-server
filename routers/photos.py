import os
import uuid

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, JSONResponse

from ai.inference import classify
from database.config import get_db
from database.models import Photo, Flower, Picture

from loguru import logger

router = APIRouter()


# 사진 업로드 후 꽃 분류
@router.post("/photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # 서버 로컬 스토리지에 이미지 저장
        UPLOAD_DIR = "./photo"

        content = await file.read()
        logger.info(f"original filename = {file.filename}")
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
    except Exception as e:
        logger.warning(f"Upload and Classify Error : {str(e)}")
        return JSONResponse(content={"error": "꽃 사진을 분류하는데 오류가 발생했습니다. 다시 시도해 주세요."}, status_code=400)


# 사진 타입 변경 (사용자가 사진 최종 선택)
@router.put("/photo/{photo_id}/{flower_type}")
async def update_photo_type(photo_id: int, flower_type: str, db: Session = Depends(get_db)):
    db.query(Photo).filter_by(photo_id=photo_id).update({"type": flower_type})
    db.commit()
    return db.query(Photo).filter_by(photo_id=photo_id).first()


# 사진 가져오기
@router.get("/photo/{photo_id}")
async def get_photo_by_id(photo_id, db: Session = Depends(get_db)):
    try:
        return db.query(Photo).filter_by(photo_id=photo_id).first()
    except Exception as e:
        logger.warning(f"Photo fetch error : {str(e)}")
        return JSONResponse(content={"error": "꽃 사진을 가져오는데 오류가 발생했습니다."}, status_code=400)


# 사진 -> 그림 변환
@router.get("/drawing/{photo_id}")
async def create_picture(photo_id: int, db: Session = Depends(get_db)):
    try:
        # 그림 변환
        # 그림 디비 저장
        db_picture: Picture = Picture(src="unknown")
        db.add(db_picture)
        db.commit()
        db.refresh(db_picture)

        return db_picture
    except Exception as e:
        logger.warning(f"Drawing error : {str(e)}")
        return JSONResponse(content={"error": "꽃 사진을 그림으로 변환하는데 오류가 발생했습니다. 다시 시도해 주세요."}, status_code=400)


# 사진 다운로드
@router.get("/download/photo/{photo_id}")
async def download_photo(photo_id: int, db: Session = Depends(get_db)):
    try:
        find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
        return FileResponse(find_photo.src)
    except Exception as e:
        logger.warning(f"Photo download error : {str(e)}")
        return JSONResponse(content={"error": "꽃 사진을 저장하는데 오류가 발생했습니다. 다시 시도해 주세요."}, status_code=400)