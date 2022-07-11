import json
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from database.models import Flower

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, "../secrets.json")
secrets = json.loads(open(SECRET_FILE).read())

DB = secrets["DB"]
S3 = secrets["S3"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding="utf-8"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# flower_list = [
#     Flower(kor_name="얼레지", eng_name="Erythronium japonicum", flower_language="바람난 여인"),
#     Flower(kor_name="노루귀", eng_name="Hepatica", flower_language="인내"),
#     Flower(kor_name="애기똥풀", eng_name="Greater celandine", flower_language="엄마의 사랑과 정성"),
#     Flower(kor_name="제비꽃", eng_name="Violet", flower_language="작은 사랑"),
#     Flower(kor_name="민들레", eng_name="Dandelion", flower_language="행복과 감사"),
#     Flower(kor_name="붓꽃", eng_name="Iris", flower_language="좋은 소식"),
#     Flower(kor_name="할미꽃", eng_name="Pasque flower", flower_language="슬픈 추억"),
#     Flower(kor_name="깽깽이풀", eng_name="Twinleaf", flower_language="안심하세요"),
#     Flower(kor_name="삼지구엽초", eng_name="Epimedium koreanum", flower_language="당신을 붙잡아두는 비밀"),
#     Flower(kor_name="현호색", eng_name="Corydale", flower_language="보물 주머니"),
#
#     Flower(kor_name="은방울꽃", eng_name="Lily of the valley", flower_language="섬세함"),
#     Flower(kor_name="복수꽃", eng_name="Adonis", flower_language="영원한 행복"),
#     Flower(kor_name="비비추", eng_name="Hosta", flower_language="좋은 소식"),
#     Flower(kor_name="동자꽃", eng_name="Dongja flower", flower_language="기다림"),
#     Flower(kor_name="곰취", eng_name="Gomchwi", flower_language="보물"),
#     Flower(kor_name="패랭이꽃", eng_name="Gilly flower", flower_language="재능"),
#     Flower(kor_name="맥문동", eng_name="Liriope platyphylla", flower_language="기쁨의 연속"),
#
#     Flower(kor_name="물봉선", eng_name="Hepatica", flower_language="인내"),
#     Flower(kor_name="애기똥풀", eng_name="Greater celandine", flower_language="엄마의 사랑과 정성"),
#     Flower(kor_name="제비꽃", eng_name="Violet", flower_language="작은 사랑"),
#
#     Flower(kor_name="민들레", eng_name="Dandelion", flower_language="행복과 감사"),
#     Flower(kor_name="붓꽃", eng_name="Iris", flower_language="좋은 소식"),
#     Flower(kor_name="할미꽃", eng_name="Pasqueflower", flower_language="슬픈 추억"),
#     Flower(kor_name="깽깽이풀", eng_name="Twinleaf", flower_language="안심하세요"),
# ]
