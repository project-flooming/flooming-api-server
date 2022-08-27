from pydantic import BaseModel


class GalleryRequest(BaseModel):
    photo_id: int
    picture_id: int
    comment: str


class GalleryResponse(BaseModel):
    gallery_id: int
    photo_id: int
    picture_id: int
    comment: str


class PictureRequest(BaseModel):
    photo_id: int


class ReportForm(BaseModel):
    gallery_id: int
    detail: str

