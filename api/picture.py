from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from deep_learning.inference import drawing
from database.config import get_db
from database.curd import find_photo, save, find_picture, paging
from database.models import Picture, Gallery
from database.schemas import GalleryDto, PictureRequest

router = APIRouter()


# 사용자가 선택한 타입으로 사전 업데이트 및 사진 -> 그림 변환
@router.post("/picture")
def create_picture(form: PictureRequest, db: Session = Depends(get_db)):
    img_src = find_photo(db, form.photo_id).saved_path

    # 그림 변환
    drawing(img_src)

    # 그림 디비 저장
    picture_save_path = "./picture/" + img_src.split('/')[-1]
    saved_picture = save(db, Picture(saved_path=picture_save_path, photo_id=form.photo_id))

    return {
        "photo_id": form.photo_id,
        "picture_id": saved_picture.picture_id
    }


# 갤러리 - 사진/그림 업로드
@router.post("/gallery")
def create_gallery(form: GalleryDto, db: Session = Depends(get_db)):
    save(db, Gallery(photo_id=form.photo_id, picture_id=form.picture_id, comment=form.comment))
    return {"result": paging(db)}


# 갤러리 - 사진/그림 리스트 반환
@router.get("/gallery")
def get_all_gallery(page: int, db: Session = Depends(get_db)):
    return {"result": paging(db, page)}


# 그림 조회 및 다운로드
@router.get("/picture/{picture_id}")
def get_picture(picture_id: int, db: Session = Depends(get_db)):
    return FileResponse(find_picture(db, picture_id).src)
