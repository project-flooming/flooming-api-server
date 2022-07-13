from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import Picture, Gallery, Photo
from database.schemas import GalleryRequest

router = APIRouter()


# 갤러리 - 사진/그림 업로드
@router.post("/picture")
async def create_gallery(form: GalleryRequest, db: Session = Depends(get_db)):
    find_photo: Photo = db.query(Photo).filter_by(photo_id=form.photo_id).first()
    find_picture: Picture = db.query(Picture).filter_by(picture_id=form.picture_id).first()

    db_gallery = Gallery(photo_src=find_photo.src, picture_src=find_picture.src, comment=form.comment)

    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)

    return db_gallery


# 갤러리 - 사진/그림 리스트 반환
@router.get("/gallery")
async def get_all_gallery(db: Session = Depends(get_db)):
    result = db.query(Gallery).all()
    return result


# 그림 다운로드
@router.get("/download/picture")
async def download_picture():
    return True
