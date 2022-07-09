import boto3
from loguru import logger
from config import DDB


def dynamo_db():
    try:
        dynamodb = boto3.resource("dynamodb",
                                  region_name="ap-northeast-2",
                                  aws_access_key_id=f"{DDB['access_key']}",
                                  aws_secret_access_key=f"{DDB['secret_key']}")
    except Exception as e:
        logger.error(f"ddb is not connected : {str(e)}")
    else:
        logger.info("dynamoDB is connected")
        return dynamodb.Table("flooming")
