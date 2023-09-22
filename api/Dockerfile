FROM docker.io/library/python:3.11-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache ffmpeg=6.0-r15 wget=1.21.4-r0

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install yandex-speechkit==1.3.3 --no-deps --no-cache-dir

COPY . .

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD wget --quiet --tries=1 --spider http://localhost:8000/ || exit 1

CMD [ "python3", "-m", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0" ]
