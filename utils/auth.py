import datetime

import jwt
from fastapi import HTTPException
from starlette.requests import Request

from utils.config import secrets

SECRET_KEY = secrets["jwt_key"]


def login_check(request: Request):
    token = request.cookies.get('token')
    if token is None:
        raise HTTPException(status_code=401, detail="로그인을 먼저 해주세요")
    validate_token(token)


def create_token():
    valid_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
    return jwt.encode({'exp': valid_time}, SECRET_KEY, algorithm='HS256')


def validate_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms='HS256')
    except jwt.ExpiredSignatureError or jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="로그인을 먼저 해주세요")

