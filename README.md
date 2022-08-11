# Flooming-Server

## 기술 스택
Framework
- FastAPI (Python)

Database
- MySQL

ORM
- SQLAlchemy

Dependencies
- loguru (Logging)

Deployment
- AWS EC2 (NginX)
- AWS RDS
- AWS Route 53

## 설치
```pip install -r requirements.txt```

## 서버 실행
main.py 실행 <br>
or
```uvicorn main:app --reload``` <br>
or
```python -m uvicorn main:app --reload``` <br>
실행 포트는 8000
/docs로 접속시 swagger 문서 확인 가능


