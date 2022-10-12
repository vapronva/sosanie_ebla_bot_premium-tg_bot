from fastapi import FastAPI
from pydantic import BaseModel
from config import Config
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

CONFIG = Config()

app = FastAPI(
    debug=True,
    title="",
    version="0.1.0",
    contact=BaseModel(email=CONFIG.get_api_contact_email()),
)
