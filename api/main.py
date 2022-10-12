from fastapi import FastAPI
from pydantic import BaseModel
from config import Config
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

CONFIG = Config()

app = FastAPI(
    debug=logging.DEBUG,
    title="",
    version="0.1.0",
    contact=BaseModel(email=CONFIG.get_api_contact_email()),
)

@app.get("/")
def read_root():
    return None

@app.get("/allowed")
def is_user_allowed(user_id: int):
    return None

@app.post("/tts/request")
def request_tts(user_id: int, query: str):
    return None
