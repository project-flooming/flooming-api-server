
from loguru import logger
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.flowers import flower_list
from database.models import Flower, Gallery, Admin
from database.schemas import GalleryResponse


# 공통 CRUD
def save(db: Session, entity):
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def find(db: Session, entity, entity_id: int):
    return db.query(entity).get(entity_id)


def find_all(db: Session, entity) -> list:
    return db.query(entity).all()


def delete(db: Session, entity):
    db.delete(entity)
    db.commit()


# 대표 꽃
def set_represent_flowers(db: Session):
    for flower in flower_list:
        if get_represent_flower(db, flower.kor_name) is None:
            db.add(flower)
            logger.info("분류용 꽃 데이터 세팅 = {}", flower.kor_name)
    db.commit()


def get_represent_flower(db: Session, kor_name: str) -> Flower:
    return db.query(Flower).filter_by(kor_name=kor_name).first()


# 갤러리
def paging(db: Session, page=0):
    unit_per_page = 5
    offset = page * unit_per_page
    result_from_db = db.query(Gallery).filter_by(is_reported=False)\
        .order_by(desc(Gallery.created_time)).offset(offset).limit(unit_per_page).all()
    return [
        GalleryResponse(
            gallery_id=post.gallery_id,
            photo_id=post.photo_id,
            picture_id=post.picture_id,
            comment=post.comment
        )
        for post in result_from_db
    ]


# 관리자
def set_admin(db: Session, password):
    if get_admin(db) is None:
        db.add(Admin(password=password))
        db.commit()


def get_admin(db: Session):
    return db.query(Admin).first()



