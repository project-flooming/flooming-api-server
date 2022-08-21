from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.config import get_db
from database.curd import save, find_gallery
from database.models import Report
from database.schemas import ReportForm
from service.slack_alarm import send_slack_alarm

router = APIRouter()

@router.post("/report")
def report(form: ReportForm, db: Session = Depends(get_db)):
    find_gallery(db, form.gallery_id).is_reported = True
    new_report = save(db, Report(gallery_id=form.gallery_id, detail=form.detail))
    send_slack_alarm(new_report)