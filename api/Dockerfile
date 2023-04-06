FROM python:3.11-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache ffmpeg=5.1.3-r0

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

USER 1027

COPY . .

CMD [ "python3", "-m", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0" ]
