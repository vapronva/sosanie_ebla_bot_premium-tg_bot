FROM python:3.10-alpine

USER 1027

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0" ]
