from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
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
from YandexSpeechkitTTS import YandexTTS as SpeechKitTTS
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
    ("tinkoff", "ru", "alyona", None, "Алёна (обычная)"),
    ("tinkoff", "ru", "alyona", "sad", "Алёна (грустная)"),
    ("tinkoff", "ru", "alyona", "funny", "Алёна (смешная)"),
    ("tinkoff", "ru", "alyona", "flirt", "Алёна (флирт)"),
    ("tinkoff", "ru", "dorofeev", "neutral", "Дорофеев (нейтральный)"),
    ("tinkoff", "ru", "dorofeev", "drama", "Дорофеев (драматичный)"),
    ("tinkoff", "ru", "dorofeev", "comedy", "Дорофеев (комедия)"),
    ("tinkoff", "ru", "dorofeev", "info", "Дорофеев (новости)"),
    ("tinkoff", "ru", "dorofeev", "tragedy", "Дорофеев (трагедия)"),
    ("tinkoff", "ru", "maxim", None, "Максим (обычный)"),
    ("yandex", "de", "lea", None, "Леа (обычная)"),
    ("yandex", "en", "john", None, "Джонн (обычный)"),
    ("yandex", "kk", "amira", None, "Амира (обычная)"),
    ("yandex", "kk", "madi", None, "Мади (обычный)"),
    ("yandex", "ru", "alena", "neutral", "Алёна (нейтральная)"),
    ("yandex", "ru", "alena", "good", "Алёна (радостная)"),
    ("yandex", "ru", "filipp", None, "Филипп (обычный)"),
    ("yandex", "ru", "ermil", "neutral", "Ермил (нейтральный)"),
    ("yandex", "ru", "ermil", "good", "Ермил (радостный)"),
    ("yandex", "ru", "jane", "neutral", "Джейн (нейтральная)"),
    ("yandex", "ru", "jane", "good", "Джейн (радостная)"),
    ("yandex", "ru", "jane", "evil", "Джейн (раздражённая)"),
    ("yandex", "ru", "madirus", None, "Мадирус (обычный)"),
    ("yandex", "ru", "omazh", "neutral", "Омаж (нейтральная)"),
    ("yandex", "ru", "omazh", "evil", "Омаж (раздражённая)"),
    ("yandex", "ru", "zahar", "neutral", "Захар (нейтральный)"),
    ("yandex", "ru", "zahar", "good", "Захар (радостный)"),
    ("yandex", "uz", "nigora", None, "Нигора (обычная)"),
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
    if "TelegramBot" not in request.headers.get("User-Agent"):
        return False
    return True


class ErrorCustomBruhher(Exception):
    def __init__(self, response: DefaultResponseModel, statusCode: int) -> None:
        self.response = response
        self.statusCode = statusCode


@app.exception_handler(ErrorCustomBruhher)
def custom_error_bruhher(request: Request, exc: ErrorCustomBruhher) -> JSONResponse:
    return JSONResponse(status_code=exc.statusCode, content=exc.response.dict())


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return DefaultResponseModel(error=None, result=None)


@app.get(
    "/allowed", response_model=DefaultResponseModel, status_code=status.HTTP_200_OK
)
def is_user_allowed(request: Request, user_id: int):
    if not check_proper_headers(request):
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_403_FORBIDDEN,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="FORBIDDEN_BALLS",
                    description="You are not authorized to access this resource",
                ),
                result=None,
            ),
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


@app.get("/tts/voice/{request_id}/{voice_id}.ogg", status_code=status.HTTP_200_OK)
def voice_message_server(request: Request, request_id: str, voice_id: str):
    if not check_proper_user_agent(request):
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_403_FORBIDDEN,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="FORBIDDEN_NUTS",
                    description="You are not authorized to access this resource",
                ),
                result=None,
            ),
        )
    userRequest = DB.get_request(request_id)
    if not userRequest:
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_404_NOT_FOUND,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="REQUEST_NOT_FOUND",
                    description="No such request found in database or it has expired",
                ),
                result=None,
            ),
        )
    selectedVoice = next(
        (x for x in userRequest["tts"] if x["voice_id"] == voice_id), None
    )
    if not selectedVoice:
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_404_NOT_FOUND,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="VOICE_NOT_FOUND",
                    description="No such voice message found in the request",
                ),
                result=None,
            ),
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
    elif selectedVoice.additionalData.company == "yandex":
        ytts = SpeechKitTTS(
            voice=selectedVoice.additionalData.speakerName,
            speed=1.0,
            audioFormat="oggopus",
            sampleRateHertz=48000,
            folderId=CONFIG.get_yandex_speechkit_folderid(),
            emotion=selectedVoice.additionalData.speakerEmotion,
        )
        ytts.IAMGen(CONFIG.get_yandex_speechkit_apitoken())
        ytts.generate(userRequest.get("content"))
        ytts.writeData(outputFile)
    if not outputFile.exists():
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_404_NOT_FOUND,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="VOICE_PROVIDER_NOT_FOUND",
                    description="No such voice provider found in available TTS models",
                ),
                result=None,
            ),
        )
    ffmpy.FFmpeg(
        global_options="-y -loglevel quiet",
        inputs={str(outputFile): None},
        outputs={
            f"./voice_messages_storage/{voice_id}.ogg": "-acodec libopus -ac 1 -ar 48000 -b:a 128k -vbr off"
        },
    ).run()
    return FileResponse(outputFile.with_suffix(".ogg"))


@app.post(
    "/tts/request",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_201_CREATED,
)
def request_tts(request: Request, body: TTSRequestBodyModel):
    requestID = str(uuid.uuid4())
    if not check_proper_headers(request):
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_403_FORBIDDEN,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="FORBIDDEN_BALLS",
                    description="You are not authorized to access this resource",
                ),
                result=None,
            ),
        )
    ttsMessages = []
    for voice in AVAILABLE_VOICES:
        company_slug = "T" if voice[0] == "tinkoff" else "Y"
        voice_id = str(uuid.uuid4())
        ttsMessages.append(
            {
                "url": f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.ogg",
                "title": f"[{voice[1].upper()}] {voice[4]} [{company_slug}]",
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


@app.options(
    "/allowed",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_200_OK,
)
def change_user_allowance(request: Request, user_id: str, allowed_status: bool):
    if not check_proper_headers(request):
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_403_FORBIDDEN,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="FORBIDDEN_BALLS",
                    description="You are not authorized to access this resource",
                ),
                result=None,
            ),
        )
    try:
        DB.set_user_allowance(user_id, allowed_status)
    except Exception as e:
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="DB_UPDATE_ERROR",
                    description="An error occurred while updating user's allowance status",
                ),
                result=None,
            ),
        )
    USER_ALLOWANCE = False
    if DB.get_user_allowed(user_id):
        USER_ALLOWANCE = True
    return DefaultResponseModel(
        error=None,
        result=UserAllowanceResultModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=UserAllowedModel(allowed=USER_ALLOWANCE),
        ),
    )
