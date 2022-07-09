from pydantic import BaseModel

'''
fastAPI 공식문서에서 발췌
여기서 말하는 schemas 는 pydantic 으로 만든 일종의 DTO 개념임
'''


class RequestPhoto(BaseModel):
    id: int
    title: str
    src: str


# 그려진 그림과 사진을 갤러리에 업로드
class ResponsePicture(BaseModel):
    photo_src: str
    picture_src: str
    comment: str
    
    class Config:
        orm_mode = True