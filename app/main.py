import uvicorn
from fastapi import FastAPI, UploadFile
from app.database import SessionLocal, engine
from app import models

# 데이터베이스 스키마 생성
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"안녕하세요": "꽃분이 입니다."}


# 사진 업로드
@app.post("/photo")
async def upload_photo(file: UploadFile):
    return {"filename" : file.filename}


@app.get("/test")
async def test():
    print("요청이 와써용")
    return {"테스트" : "입니다"}



if __name__ == "__main__":
    uvicorn.run(app)
