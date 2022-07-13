from pydantic import BaseModel


class GalleryRequest(BaseModel):
    photo_id: int
    picture_id: int
    comment: str

