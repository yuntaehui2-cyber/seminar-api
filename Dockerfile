# 1. 파이썬 3.12 슬림 버전 이미지를 기반으로 시작합니다.
FROM python:3.12-slim

# 2. 컨테이너 내부의 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 3. 패키지 설치를 위해 의존성 파일만 먼저 복사합니다. (캐싱 활용)
COPY requirements.txt .

# 4. pip를 최신으로 업데이트하고 필요한 라이브러리들을 설치합니다.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. 현재 프로젝트의 모든 소스 코드를 컨테이너 내부로 복사합니다.
COPY . .

# 6. Flask가 사용할 5000번 포트를 외부로 개방합니다.
EXPOSE 5000

# 7. Gunicorn을 이용해 WSGI 서버로 Flask 앱을 구동합니다.
# (app 폴더 안의 __init__.py 등에서 생성될 Flask 객체를 실행하도록 설정)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
