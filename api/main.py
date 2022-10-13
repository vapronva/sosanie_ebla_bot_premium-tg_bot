from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from models import (
    DefaultResponseModel,
    DefaultErrorModel,
    UserAllowanceResultModel,
    UserAllowedModel,
    TTSRequestBodyModel,
    VoiceMessagesTTSResultModel,
    VoiceMessageTTSInlineModel,
    AdditionalDataModel,
)
from TinkoffVoicekitTTS import process_text_to_speech as tinkoff_tts
from config import Config
import logging
import uuid
from db import DB
import ffmpy

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

CONFIG = Config()

DB = DB(CONFIG.get_db_mongodb_uri())

AVAILABLE_VOICES = [
    ("tinkoff", "ru", "alyona", None, "Алёна (обычный)"),
    ("tinkoff", "ru", "alyona", "sad", "Алёна (грустный)"),
    ("tinkoff", "ru", "alyona", "funny", "Алёна (смешной)"),
    ("tinkoff", "ru", "alyona", "flirt", "Алёна (флирт)"),
    ("tinkoff", "ru", "dorofeev", "neutral", "Дорофеев (нейтральный)"),
    ("tinkoff", "ru", "dorofeev", "drama", "Дорофеев (драматичный)"),
    ("tinkoff", "ru", "dorofeev", "comedy", "Дорофеев (комедия)"),
    ("tinkoff", "ru", "dorofeev", "info", "Дорофеев (новости)"),
    ("tinkoff", "ru", "dorofeev", "tragedy", "Дорофеев (трагедия)"),
    ("tinkoff", "ru", "maxim", None, "Максим (обычный)"),
]

app = FastAPI(
    debug=logging.DEBUG,
    title="Sosanie Ebla Bot Premium API",
    version="0.1.0",
    contact=BaseModel(email=CONFIG.get_api_contact_email()),
)


def check_proper_headers(request: Request) -> bool:
    if request.headers.get("X-API-Token") != CONFIG.get_vprw_api_key():
        return False
    return True


def check_proper_user_agent(request: Request) -> bool:
    if not "TelegramBot" in request.headers.get("User-Agent"):
        return False
    return True


@app.get("/")
def read_root():
    return DefaultResponseModel(error=None, result=None)


@app.get("/allowed", response_model=DefaultResponseModel)
def is_user_allowed(request: Request, user_id: int):
    if not check_proper_headers(request):
        return DefaultResponseModel(
            error=DefaultErrorModel(
                name="FORBIDDEN_BALLS",
                description="You are not authorized to access this resource",
            ),
            result=None,
        )
    USER_ALLOWANCE = False
    if DB.get_user_allowed(user_id):
        USER_ALLOWANCE = True
    return DefaultResponseModel(
        error=None,
        result=UserAllowanceResultModel(
            requestID=str(uuid.uuid4()),
            cacheTime=10,
            data=UserAllowedModel(allowed=USER_ALLOWANCE),
        ),
    )


def generate_selected_voice_tinkoff(additionalData: AdditionalDataModel) -> str:
    if additionalData.speakerEmotion:
        return f"{additionalData.speakerName}:{additionalData.speakerEmotion}"
    return additionalData.speakerName


@app.get("/tts/voice/{request_id}/{voice_id}.ogg")
def voice_message_server(request: Request, request_id: str, voice_id: str):
    userRequest = DB.get_request(request_id)
    if not userRequest:
        return (
            DefaultResponseModel(
                error=DefaultErrorModel(
                    name="REQUEST_NOT_FOUND",
                    description="No such request found in database or it has expired",
                ),
                result=None,
            ),
            404,
        )
    selectedVoice = next(
        (x for x in userRequest["tts"] if x["voice_id"] == voice_id), None
    )
    if not selectedVoice:
        return (
            DefaultResponseModel(
                error=DefaultErrorModel(
                    name="VOICE_NOT_FOUND",
                    description="No such voice found in request",
                ),
                result=None,
            ),
            404,
        )
    selectedVoice = VoiceMessageTTSInlineModel(**selectedVoice)
    outputFile = Path(f"./voice_messages_storage/{voice_id}.wav")
    if selectedVoice.additionalData.company == "tinkoff":
        tinkoff_tts(
            text=userRequest.get("content"),
            selected_voice=generate_selected_voice_tinkoff(
                selectedVoice.additionalData
            ),
            output_file=outputFile,
        )
        ffmpy.FFmpeg(
            inputs={str(outputFile): None},
            outputs={f"./voice_messages_storage/{voice_id}.ogg": "-acodec libvorbis"},
        ).run()
        return FileResponse(outputFile.with_suffix(".ogg"))
    return (
        DefaultResponseModel(
            error=DefaultErrorModel(
                name="VOICE_PROVIDER_NOT_FOUND",
                description="No such voice provider found in available TTS models",
            ),
            result=None,
        ),
        404,
    )


@app.post("/tts/request", response_model=DefaultResponseModel)
def request_tts(request: Request, body: TTSRequestBodyModel):
    requestID = str(uuid.uuid4())
    if not check_proper_headers(request):
        return DefaultResponseModel(
            error=BaseModel(
                name="FORBIDDEN_BALLS",
                description="You are not authorized to access this resource",
            ),
            result=None,
        )
    ttsMessages = []
    for voice in AVAILABLE_VOICES:
        voice_id = str(uuid.uuid4())
        ttsMessages.append(
            {
                "url": f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.ogg",
                "title": f"[{voice[1].upper()}] {voice[4]}",
                "caption": None,
                "voice_id": voice_id,
                "additionalData": {
                    "speakerLang": voice[1],
                    "speakerName": voice[2],
                    "speakerEmotion": voice[3],
                    "company": voice[0],
                },
            }
        )
    DB.create_user_content(
        user_id=body.user_id, content=body.query, requestID=requestID, tts=ttsMessages
    )
    return DefaultResponseModel(
        error=None,
        result=VoiceMessagesTTSResultModel(
            requestID=requestID,
            cacheTime=10,
            data=ttsMessages,
        ),
    )
