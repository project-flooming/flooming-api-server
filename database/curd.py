from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.models import Photo, Flower, Picture, Gallery
from database.schemas import GalleryDto


def save(db: Session, entity):
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def find_photo(db: Session, entity_id: int) -> Photo:
    return db.query(Photo).get(entity_id)


def find_picture(db: Session, entity_id: int) -> Picture:
    return db.query(Picture).get(entity_id)


def get_represent_flower(db: Session, kor_name: str) -> Flower:
    return db.query(Flower).filter_by(kor_name=kor_name).first()


def paging(db, page=0):
    unit_per_page = 5
    offset = page * unit_per_page
    result_from_db = db.query(Gallery).order_by(desc(Gallery.created_time)).offset(offset).limit(unit_per_page).all()
    return [
        GalleryDto(photo_id=post.photo_id, picture_id=post.picture_id, comment=post.comment)
        for post in result_from_db
    ]
