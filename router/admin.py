from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.params import Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, Response, RedirectResponse

from database.config import get_db
from database.curd import save, find, delete, get_admin, find_all
from database.models import Report, Gallery
from database.schemas import ReportForm, LoginForm
from utils.auth import create_token, login_check
from utils.photo import delete_image
from utils.alarm import send_slack_alarm


router = APIRouter()
templates = Jinja2Templates(directory="./static/templates")


# 관리자 페이지 접근
@router.get("/admin")
def admin_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 관리자 로그인
@router.post("/login")
def login(
        request: Request,
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    admin = get_admin(db)
    context = {"request": request, "result": True}

    if admin.password != password:
        context["result"] = False
        context["error"] = "비밀번호가 틀립니다."
        return templates.TemplateResponse("login.html", context)

    access_token = create_token()
    response = RedirectResponse(url="/reports")
    response.set_cookie(key="token", value=access_token, httponly=True)
    return response


# 사용자 - 갤러리 신고
@router.post("/report")
def report(form: ReportForm, db: Session = Depends(get_db)):
    find(db, entity=Gallery, entity_id=form.gallery_id).is_reported = True
    new_report = save(db, Report(gallery_id=form.gallery_id, detail=form.detail))
    send_slack_alarm(new_report)
    return {"result": "success"}


# 관리자 - 해당 갤러리 재업로드
@router.post("/re-upload/{report_id}")
def re_upload(request: Request, report_id: int, db: Session = Depends(get_db)):
    login_check(request)
    find_report = find(db, Report, report_id)
    find(db, Gallery, find_report.gallery_id).is_reported = False
    delete(db, find_report)
    return RedirectResponse(url="/reports")


# 관리자 - 신고 목록들 조회
@router.post("/reports")
def get_all_reports(request: Request, db: Session = Depends(get_db)):
    login_check(request)
    context = {"request": request}

    find_reports: List[Report] = find_all(db, Report)
    result = []
    if find_reports:
        for r in find_reports:
            result.append({
                "report_id": r.report_id,
                "gallery_id": r.gallery_id,
                "photo_id": r.gallery.photo_id,
                "picture_id": r.gallery.picture_id,
                "comment": r.gallery.comment,
                "reason": r.detail,
                "created_time": r.created_time
            })
    context["reports"] = result

    return templates.TemplateResponse("main.html", context)


# 관리자 - 해당 갤러리 삭제
@router.post("/delete/report/{report_id}")
def delete_gallery(request: Request, report_id: int, db: Session = Depends(get_db)):
    login_check(request)

    find_report: Report = find(db, Report, report_id)
    gallery = find_report.gallery

    delete_image(gallery.photo.saved_path)
    delete_image(gallery.picture.saved_path)

    delete(db, gallery)
    delete(db, find_report)

    return RedirectResponse(url="/reports")

