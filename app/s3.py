import boto3
from fastapi import UploadFile

from config import S3

bucket_name = "flooming-s3"


def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id=f"{S3['access_key']}",
            aws_secret_access_key=f"{S3['secret_key']}",
        )
    except Exception as e:
        print(f"s3 connection error = {e}")
    else:
        print(f"s3 connected")
        return s3


class ImageStorage:
    def __init__(self):
        self.s3 = s3_connection()

    def upload(self, file: UploadFile):
        try:
            self.s3.upload_fileobj(file.read(), bucket_name, "test.png")
        except Exception as e:
            print(f"imageStorage error = {e}")
            return "src"
        return self.get_src(file.filename)

    def get_src(self, filename):
        location = self.s3.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
        return f"https://{bucket_name}.s3.{location}.amazonaws.com/{filename}.jpg"



