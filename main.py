from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"안녕하세요": "꽃분이 입니다."}

