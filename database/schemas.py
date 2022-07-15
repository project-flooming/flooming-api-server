from pydantic import BaseModel


class GalleryRequest(BaseModel):
    photo_id: int
    picture_id: int
    comment: str


class GalleryResponse(BaseModel):
    photo_src: str
    picture_src: str
    comment: str


class PictureRequest(BaseModel):
    photo_id: int
    flower_type: str
