import datetime
import os
import random

from fastapi import HTTPException
from loguru import logger


def validate(classify_result, src):
    prob_list = [result["probability"] for result in classify_result]
    max_prob = max(prob_list)
    if max_prob >= 90:
        return classify_result[0]
    elif max_prob <= 50:
        delete_photo(src)
        raise HTTPException(status_code=400, detail="알아볼 수 없는 사진이에요!")
    return classify_result[0]


def upload(file):
    try:
        UPLOAD_DIR = "./image/photo"
        content = file.file.read()
        # logger.info(f"original filename = {file.filename}")
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{random.randint(0, 1000)}.jpg"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(content)
        src = f"{UPLOAD_DIR}/{filename}"
        return filename, src
    except Exception as e:
        logger.warning(f"photo upload fail = {str(e)}")
        raise HTTPException(status_code=500, detail="서버에 문제가 생긴 것 같아요!")


def delete_photo(src):
    os.remove(src)