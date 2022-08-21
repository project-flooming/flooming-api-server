from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.config import get_db
from database.curd import save, find, delete
from database.models import Report, Gallery, Photo, Picture
from database.schemas import ReportForm
from service.photo import delete_image
from service.slack_alarm import send_slack_alarm

router = APIRouter()


@router.post("/report")
def report(form: ReportForm, db: Session = Depends(get_db)):
    find(db, entity=Gallery, entity_id=form.gallery_id).is_reported = True
    new_report = save(db, Report(gallery_id=form.gallery_id, detail=form.detail))
    send_slack_alarm(new_report)
    return {"result": "complete"}


@router.delete("/gallery/{gallery_id}")
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = find(db, entity=Gallery, entity_id=gallery_id)
    photo = find(db, entity=Photo, entity_id=gallery.photo_id).saved_path
    picture = find(db, entity=Picture, entity_id=gallery.picture_id).saved_path
    delete_image(photo)
    delete_image(picture)
    delete(db, gallery)

