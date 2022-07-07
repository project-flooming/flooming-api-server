from pydantic import BaseModel

'''
fastAPI 공식문서에서 발췌
여기서 말하는 schemas 는 pydantic 으로 만든 일종의 DTO 개념임
'''


# 사진 -> 그림 변환후 내려주기
class PictureDto(BaseModel):
    src: str


# 그려진 그림과 사진을 갤러리에 업로드
class GalleryDto(BaseModel):
    photo_src: str
    picture_src: str
    comment: str