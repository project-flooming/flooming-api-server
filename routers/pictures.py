from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.config import get_db
from database.models import Picture, Gallery, Photo
from database.schemas import GalleryRequest
from loguru import logger

router = APIRouter()


# 갤러리 - 사진/그림 업로드
@router.post("/picture")
async def create_gallery(form: GalleryRequest, db: Session = Depends(get_db)):
    try:
        find_photo: Photo = db.query(Photo).filter_by(photo_id=form.photo_id).first()
        find_picture: Picture = db.query(Picture).filter_by(picture_id=form.picture_id).first()

        db_gallery = Gallery(photo_src=find_photo.src, picture_src=find_picture.src, comment=form.comment)

        db.add(db_gallery)
        db.commit()
        db.refresh(db_gallery)

        return db_gallery
    except Exception as e:
        logger.warning(f"Gallery upload error : {str(e)}")
        return JSONResponse(content={"error": "갤러리에 그림을 전시하는데 오류가 발생했습니다. 다시 시도해 주세요."}, status_code=400)


# 갤러리 - 사진/그림 리스트 반환
@router.get("/gallery")
async def get_all_gallery(page: int, db: Session = Depends(get_db)):
    try:
        unit_per_page = 5
        offset = page * unit_per_page
        return db.query(Gallery).order_by(desc(Gallery.created_time)).offset(offset).limit(unit_per_page).all()
    except Exception as e:
        logger.warning(f"Gallery list fetching error : {str(e)}")
        return JSONResponse(content={"error": "갤러리 그림들을 가져오는데 오류가 발생했습니다. 다시 시도해 주세요."}, status_code=400)


# 그림 다운로드
@router.get("/download/picture")
async def download_picture():
    return True
