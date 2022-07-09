from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String
from app.database import Base

'''
fastAPI 공식문서에서 발췌
SQLAlchemy는 데이터베이스 스키마를 models로 부름
'''


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    src = Column(String(255))  # 이미지 저장 경로
    created_time = Column(DateTime, default=datetime.now)


class Picture(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True, index=True)
    pic_src = Column(String(255))  # 실제 사진 저장 경로
    photo_src = Column(String(255))  # 그려진 그림 저장 경로
    comment = Column(String(255))
    created_time = Column(DateTime, default=datetime.now)

