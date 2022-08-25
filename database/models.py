from datetime import datetime
from sqlalchemy import DateTime, BigInteger, Boolean, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.config import Base


class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))


class Flower(Base):
    __tablename__ = "flower"

    flower_id = Column(Integer, primary_key=True, autoincrement=True)
    kor_name = Column(String(255), default="unknown")
    eng_name = Column(String(255), default="unknown")
    flower_language = Column(String(255), default="unknown")  # 꽃말


class Photo(Base):
    __tablename__ = "photo"

    photo_id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), default="unknown")
    flower_type = Column(String(255), default="unknown")
    saved_path = Column(String(255), default="unknown")  # 이미지 저장 경로
    created_time = Column(DateTime, default=datetime.now)

    gallery = relationship("Gallery", back_populates="photo", uselist=False)


class Picture(Base):
    __tablename__ = "picture"

    picture_id = Column(BigInteger, primary_key=True, autoincrement=True)
    photo_id = Column(BigInteger)
    saved_path = Column(String(255), default="unknown")  # 그려진 그림 저장 경로
    created_time = Column(DateTime, default=datetime.now)

    gallery = relationship("Gallery", back_populates="picture", uselist=False)


class Gallery(Base):
    __tablename__ = "gallery"

    gallery_id = Column(BigInteger, primary_key=True, autoincrement=True)

    photo_id = Column(BigInteger, ForeignKey("photo.photo_id"))
    photo = relationship("Photo", back_populates="gallery", cascade="all")

    picture_id = Column(BigInteger, ForeignKey("picture.picture_id"))
    picture = relationship("Picture", back_populates="gallery", cascade="all")

    comment = Column(String(255), default="unknown")
    is_reported = Column(Boolean, default=False)
    created_time = Column(DateTime, default=datetime.now)

    report = relationship("Report", back_populates="gallery", uselist=False)


class Report(Base):
    __tablename__ = "report"
    report_id = Column(BigInteger, primary_key=True, autoincrement=True)

    detail = Column(String(255), default="unknown")
    created_time = Column(DateTime, default=datetime.now)

    gallery_id = Column(BigInteger, ForeignKey("gallery.gallery_id"))
    gallery = relationship("Gallery", back_populates="report")
