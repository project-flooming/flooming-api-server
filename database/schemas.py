from pydantic import BaseModel


class GalleryDto(BaseModel):
    photo_id: int
    picture_id: int
    comment: str


class PictureRequest(BaseModel):
    photo_id: int


class ReportForm(BaseModel):
    gallery_id: int
    detail: str
