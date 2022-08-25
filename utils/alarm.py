import datetime
import requests

from database.models import Report
from utils.config import secrets


def send_slack_alarm(new_report: Report):
    hook = secrets['slack']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title = f"[{time}] \n새로운 신고 접수!"
    content = f"\n갤러리 ID : {new_report.gallery_id} \n사유 : {new_report.detail}"

    requests.post(
        hook,
        headers={'content-type': 'application/json'},
        json={'text': title + content}
    )