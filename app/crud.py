from sqlalchemy.orm import Session
import models


def get_photo(db: Session, photo_id: int):
    return db.query(models)