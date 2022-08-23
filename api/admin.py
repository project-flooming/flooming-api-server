from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.config import get_db
from database.curd import save, find, delete
from database.models import Report, Gallery
from database.schemas import ReportForm
from service.photo import delete_image
from service.slack_alarm import send_slack_alarm

router = APIRouter()


@router.post("/report")
def report(form: ReportForm, db: Session = Depends(get_db)):
    find(db, entity=Gallery, entity_id=form.gallery_id).is_reported = True
    new_report = save(db, Report(gallery_id=form.gallery_id, detail=form.detail))
    send_slack_alarm(new_report)
    return {"result": "success"}


@router.delete("/gallery/{gallery_id}")
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = find(db, entity=Gallery, entity_id=gallery_id)
    delete_image(gallery.photo.saved_path)
    delete_image(gallery.picture.saved_path)
    delete(db, gallery)
    return {"result": "success"}

