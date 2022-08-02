from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String
from database.config import Base


class Flower(Base):
    __tablename__ = "flower"

    flower_id = Column(Integer, primary_key=True)
    kor_name = Column(String(255), default="unknown")
    eng_name = Column(String(255), default="unknown")
    flower_language = Column(String(255), default="unknown")  # 꽃말


class Photo(Base):
    __tablename__ = "photo"

    photo_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    filename = Column(String(255), default="unknown")
    type = Column(String(255), default="unknown")
    src = Column(String(255), default="unknown")  # 이미지 저장 경로
    created_time = Column(DateTime, default=datetime.now)


class Picture(Base):
    __tablename__ = "picture"

    picture_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    photo_id = Column(Integer)
    src = Column(String(255), default="unknown")  # 그려진 그림 저장 경로
    created_time = Column(DateTime, default=datetime.now)


class Gallery(Base):
    __tablename__ = "gallery"

    gallery_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    photo_id = Column(Integer, default=0)
    picture_id = Column(Integer, default=0)
    comment = Column(String(255), default="unknown")
    created_time = Column(DateTime, default=datetime.now)