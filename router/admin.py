from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.params import Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, Response, RedirectResponse

from database.config import get_db
from database.curd import save, find, delete, get_admin
from database.models import Report, Gallery
from database.schemas import ReportForm, LoginForm
from utils.auth import create_token, login_check
from utils.photo import delete_image
from utils.alarm import send_slack_alarm


router = APIRouter()
templates = Jinja2Templates(directory="./static/templates")


@router.get("/admin", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
        request: Request,
        response: Response,
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
    response.set_cookie(key="token", value=f"Bearer {access_token}", httponly=True)
    return templates.TemplateResponse("main.html", context)


@router.post("/report")
def report(form: ReportForm, db: Session = Depends(get_db)):
    find(db, entity=Gallery, entity_id=form.gallery_id).is_reported = True
    new_report = save(db, Report(gallery_id=form.gallery_id, detail=form.detail))
    send_slack_alarm(new_report)
    return {"result": "success"}


@router.delete("/gallery/{gallery_id}")
def delete_gallery(request: Request, gallery_id: int, db: Session = Depends(get_db)):
    login_check(request)

    gallery = find(db, entity=Gallery, entity_id=gallery_id)
    delete_image(gallery.photo.saved_path)
    delete_image(gallery.picture.saved_path)
    delete(db, gallery)
    return {"result": "success"}

