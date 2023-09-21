import logging
import uuid
from pathlib import Path
from typing import List, Optional

import ffmpy
import sentry_sdk
from config import Config
from db import DB as DatabaseManager
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from models import (
    AdditionalDataModel,
    CallbackDataModel,
    CallbackResponseShowTextModel,
    CallbackShowTextModelResponseModel,
    DatabaseTokenObjectModel,
    DatabaseTokenResponseOverallModel,
    DefaultErrorModel,
    DefaultResponseModel,
    SpokenVoiceModel,
    TTSRequestBodyModel,
    TTSRequestWithDirectWavBodyModel,
    UserAllowanceResultModel,
    UserAllowedModel,
    UserRequestContentDatabaseModel,
    VoiceListResponseModel,
    VoiceMessagesTTSResultModel,
    VoiceMessageTTSInlineModel,
)
from pydantic import BaseModel, HttpUrl, parse_obj_as
from requests import get as requests_get
from SberbankSalutespeechTTS import SberbankSaluteSpeechDemo
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from TinkoffVoicekitTTS import process_text_to_speech as tinkoff_tts
from VKCloudVoiceTTS import VCVoices as VKCloudVoiceVoices
from VKCloudVoiceTTS import VKCloudVoiceTTS
from YandexSpeechkitTTS import YandexTTS as SpeechKitTTS

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s",
)

CONFIG = Config()

sentry_sdk.init(
    dsn=CONFIG.get_sentry_dsn(),
    release=CONFIG.get_deployment_release(),
    environment=CONFIG.get_deployment_environment(),
    traces_sample_rate=1.0,
    enable_tracing=True,
)

DB = DatabaseManager(CONFIG.get_db_mongodb_uri())

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
    ("vk", "ru", "katherine", None, "Катерина (обычная)"),
    ("vk", "ru", "maria", None, "Мария (обычная)"),
    ("vk", "ru", "pavel", None, "Павел (обычный)"),
    ("sberbank", "ru", "nataly", None, "Наталья (обычная)"),
    ("sberbank", "ru", "boris", None, "Борис (обычный)"),
    ("sberbank", "ru", "marfa", None, "Марфа (обычная)"),
    ("sberbank", "ru", "taras", None, "Тарас (обычный)"),
    ("sberbank", "ru", "alexa", None, "Александра (обычная)"),
    ("sberbank", "ru", "sergey", None, "Сергей (обычный)"),
]

app = FastAPI(
    debug=logging.DEBUG,  # type: ignore
    title="Sosanie Ebla Bot Premium API",
    version="0.3.0",
    contact=BaseModel(email=CONFIG.get_api_contact_email()).dict(),
)

VCV_TTS = VKCloudVoiceTTS(CONFIG.get_vk_cloudvoice_servicetoken())


def check_proper_headers(request: Request, checkOnlyMasterToken: bool = False) -> bool:
    if request.headers.get("X-API-Token") != CONFIG.get_vprw_api_key():
        if (
            DB.check_token_usage(request.headers.get("X-API-Key") or "")
            and not checkOnlyMasterToken
        ):
            DB.update_token_usage(request.headers.get("X-API-Key") or "")
            return True
        logging.warning("Wrong API key detected in request for %s", request.url)
        return False
    return True


def check_proper_user_agent(request: Request) -> bool:
    if "TelegramBot" not in request.headers.get("User-Agent").__str__():
        return False
    return True


class ErrorCustomBruhher(Exception):
    def __init__(  # skipcq: PYL-W0231
        self, response: DefaultResponseModel, statusCode: int,
    ) -> None:
        self.response = response
        self.statusCode = statusCode


@app.exception_handler(ErrorCustomBruhher)
def custom_error_bruhher(request: Request, exc: ErrorCustomBruhher) -> JSONResponse:
    return JSONResponse(status_code=exc.statusCode, content=exc.response.dict())


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return DefaultResponseModel(error=None, result=None)


@app.get(
    "/allowed", response_model=DefaultResponseModel, status_code=status.HTTP_200_OK,
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
    if DB.get_user_allowed(int(user_id)):
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
    userRequest = DB.get_request(requestID=request_id)
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
    selectedVoice = next((x for x in userRequest.tts if x.voice_id == voice_id), None)
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
    outputFile = Path(f"./voice_messages_storage/{voice_id}.wav")
    if outputFile.with_suffix(".ogg").exists():
        return FileResponse(outputFile.with_suffix(".ogg"))
    if selectedVoice.additionalData.company == "tinkoff":
        try:
            tinkoff_tts(
                text=userRequest.content,
                selected_voice=generate_selected_voice_tinkoff(
                    selectedVoice.additionalData,
                ),
                output_file=outputFile,
            )
        except Exception as e:
            logging.error(e)
            raise ErrorCustomBruhher(
                statusCode=status.HTTP_503_SERVICE_UNAVAILABLE,
                response=DefaultResponseModel(
                    error=DefaultErrorModel(
                        name="TINKOFF_TTS_ERROR",
                        description="Tinkoff TTS service is unavailable at the moment",
                    ),
                    result=None,
                ),
            )
    elif selectedVoice.additionalData.company == "yandex":
        try:
            ytts = SpeechKitTTS(
                voice=selectedVoice.additionalData.speakerName,
                speed=1.0,
                audioFormat="oggopus",
                sampleRateHertz=48000,
                folderId=CONFIG.get_yandex_speechkit_folderid(),
                emotion=selectedVoice.additionalData.speakerEmotion,
            )
            ytts.IAMGen(CONFIG.get_yandex_speechkit_apitoken())
            ytts.generate(userRequest.content)
            ytts.writeData(outputFile.with_suffix(".ogg"))
            ffmpy.FFmpeg(
                global_options="-y -loglevel quiet",
                inputs={str(outputFile.with_suffix(".ogg")): None},
                outputs={
                    outputFile.with_suffix(".wav")
                    .absolute()
                    .__str__(): "-acodec pcm_s16le -ac 1 -ar 48000",
                },
            ).run()
        except Exception as e:
            logging.error(e)
            raise ErrorCustomBruhher(
                statusCode=status.HTTP_503_SERVICE_UNAVAILABLE,
                response=DefaultResponseModel(
                    error=DefaultErrorModel(
                        name="YANDEX_TTS_ERROR",
                        description="Yandex TTS service is unavailable at the moment",
                    ),
                    result=None,
                ),
            )
    elif selectedVoice.additionalData.company == "vk":
        try:
            VCV_TTS.save_audio(
                text=userRequest.content,
                voice=VKCloudVoiceVoices(selectedVoice.additionalData.speakerName),
                path=outputFile.with_suffix(".mp3"),
            )
            ffmpy.FFmpeg(
                global_options="-y -loglevel quiet",
                inputs={str(outputFile.with_suffix(".mp3")): None},
                outputs={
                    outputFile.with_suffix(".wav")
                    .absolute()
                    .__str__(): "-acodec pcm_s16le -ac 1 -ar 24000",
                },
            ).run()
        except Exception as e:
            logging.error(e)
            raise ErrorCustomBruhher(
                statusCode=status.HTTP_503_SERVICE_UNAVAILABLE,
                response=DefaultResponseModel(
                    error=DefaultErrorModel(
                        name="VKCV_TTS_ERROR",
                        description="VK TTS service is unavailable at the moment",
                    ),
                    result=None,
                ),
            )
    elif selectedVoice.additionalData.company == "sberbank":
        try:
            SberbankSaluteSpeechDemo.synthesize(
                selectedVoice=selectedVoice.additionalData.speakerName,
                text=userRequest.content,
                outputFile=outputFile,
            )
        except Exception as e:
            logging.error(e)
            raise ErrorCustomBruhher(
                statusCode=status.HTTP_503_SERVICE_UNAVAILABLE,
                response=DefaultResponseModel(
                    error=DefaultErrorModel(
                        name="SBERBANL_TTS_ERROR",
                        description="SberBank TTS service is unavailable at the moment",
                    ),
                    result=None,
                ),
            )
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
    if selectedVoice.additionalData.company in ["tinkoff", "vk", "sberbank"]:
        ffmpy.FFmpeg(
            global_options="-y -loglevel quiet",
            inputs={str(outputFile): None},
            outputs={
                outputFile.with_suffix(".ogg")
                .absolute()
                .__str__(): "-acodec libopus -ac 1 -ar 48000 -b:a 128k -vbr off",
            },
        ).run()
    return FileResponse(outputFile.with_suffix(".ogg"))


@app.get("/tts/voice/{request_id}/{voice_id}.wav", status_code=status.HTTP_200_OK)
def voice_message_wav(
    request: Request, request_id: str, voice_id: str, download: bool = False,
):
    userRequest = DB.get_request(requestID=request_id)
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
    selectedVoice = next((x for x in userRequest.tts if x.voice_id == voice_id), None)
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
    outputFile = Path(f"./voice_messages_storage/{voice_id}.wav")
    if not outputFile.exists():
        _ = requests_get(
            url=f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.ogg",
        )
    if outputFile.exists():
        if download:
            return FileResponse(
                outputFile,
                media_type="audio/wav",
                headers={
                    "Content-Disposition": f"attachment, filename=sosanieeblabotpremium-{voice_id.replace('-', '')}.wav",
                },
            )
        return FileResponse(outputFile)
    if outputFile.with_suffix(".ogg").exists() and not outputFile.exists():
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_404_NOT_FOUND,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="VOICE_IRRETRIEVABLE",
                    description="Voice message is not available in .wav format",
                ),
                result=None,
            ),
        )
    raise ErrorCustomBruhher(
        statusCode=status.HTTP_404_NOT_FOUND,
        response=DefaultResponseModel(
            error=DefaultErrorModel(
                name="FILE_NOT_FOUND",
                description="No such file found in the storage",
            ),
            result=None,
        ),
    )


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
    ttsMessages: List[VoiceMessageTTSInlineModel] = []
    for voice in AVAILABLE_VOICES:
        match voice[0]:
            case "tinkoff":
                company_slug = "T"
            case "yandex":
                company_slug = "Y"
            case "vk":
                company_slug = "V"
            case "sberbank":
                company_slug = "S"
            case _:
                company_slug = "UNDEFINED"
        voice_id = str(uuid.uuid4())
        ttsMessages.append(
            VoiceMessageTTSInlineModel(
                url=parse_obj_as(
                    HttpUrl,
                    f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.ogg",
                ),
                title=f"[{voice[1].upper()}] {voice[4]} [{company_slug}]",
                caption=None,
                voice_id=voice_id,
                additionalData=AdditionalDataModel(
                    company=voice[0],
                    speakerLang=voice[1],
                    speakerName=voice[2],
                    speakerEmotion=voice[3],
                ),
                callbackData=CallbackDataModel(
                    getVoiceTextID=f"{requestID[-12:]}-{uuid.uuid4().__str__().replace('-', '_')}",
                    publicVoiceWavUrl=parse_obj_as(
                        HttpUrl,
                        f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.wav?download=true",
                    ),
                ),
            ),
        )
    DB.create_user_content(
        UserRequestContentDatabaseModel(
            user_id=body.user_id,
            content=body.query,
            requestID=requestID,
            tts=ttsMessages,
        ),
    )
    return DefaultResponseModel(
        error=None,
        result=VoiceMessagesTTSResultModel(
            requestID=requestID,
            cacheTime=10,
            data=ttsMessages,
        ),
    )


@app.post(
    "/tts/request/wav",
    status_code=status.HTTP_201_CREATED,
)
def request_tts_wav(request: Request, body: TTSRequestWithDirectWavBodyModel):
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
    ttsMessages: List[VoiceMessageTTSInlineModel] = []
    for voice in AVAILABLE_VOICES:
        if (
            voice[0] != body.voice.company
            or voice[1] != body.voice.speakerLang
            or voice[2] != body.voice.speakerName
            or voice[3] != body.voice.speakerEmotion
        ):
            continue
        match voice[0]:
            case "tinkoff":
                company_slug = "T"
            case "yandex":
                company_slug = "Y"
            case "vk":
                company_slug = "V"
            case "sberbank":
                company_slug = "S"
            case _:
                company_slug = "UNDEFINED"
        voice_id = str(uuid.uuid4())
        ttsMessages.append(
            VoiceMessageTTSInlineModel(
                url=parse_obj_as(
                    HttpUrl,
                    f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.ogg",
                ),
                title=f"[{voice[1].upper()}] {voice[4]} [{company_slug}]",
                caption=None,
                voice_id=voice_id,
                additionalData=AdditionalDataModel(
                    company=voice[0],
                    speakerLang=voice[1],
                    speakerName=voice[2],
                    speakerEmotion=voice[3],
                ),
                callbackData=CallbackDataModel(
                    getVoiceTextID=f"{requestID[-12:]}-{uuid.uuid4().__str__().replace('-', '_')}",
                    publicVoiceWavUrl=parse_obj_as(
                        HttpUrl,
                        f"https://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{requestID}/{voice_id}.wav",
                    ),
                ),
            ),
        )
    DB.create_user_content(
        UserRequestContentDatabaseModel(
            user_id=body.user_id,
            content=body.query,
            requestID=requestID,
            tts=ttsMessages,
        ),
    )
    if len(ttsMessages) == 0:
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
    return Response(
        str(
            f"{ttsMessages[0].callbackData.publicVoiceWavUrl}"
            if ttsMessages[0].callbackData is not None
            else f"{ttsMessages[0].url}",
        ),
        status_code=status.HTTP_201_CREATED,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=sosanieeblabotpremium-{ttsMessages[0].voice_id.replace('-', '')}.wav",
        },
    )


@app.get("/callback/action/{action_id}/{callback_id}", status_code=status.HTTP_200_OK)
def answer_callback_action_sucktion(request: Request, action_id: str, callback_id: str):
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
    logging.info("Received callback action `%s` for #%s", action_id, callback_id)
    match action_id:
        case "getshwsgt":
            userRequest = DB.get_request_by_callback_data("getVoiceTextID", callback_id)
            if not userRequest:
                raise ErrorCustomBruhher(
                    statusCode=status.HTTP_404_NOT_FOUND,
                    response=DefaultResponseModel(
                        error=DefaultErrorModel(
                            name="CALLBACK_NOT_FOUND",
                            description="No such callback found in database",
                        ),
                        result=None,
                    ),
                )
            logging.info(
                "Sending text for #%s as of request #%s",
                callback_id,
                userRequest.requestID,
            )
            return DefaultResponseModel(
                error=None,
                result=CallbackShowTextModelResponseModel(
                    requestID=str(uuid.uuid4()),
                    data=CallbackResponseShowTextModel(
                        text=f'Original text: "{userRequest.content}"',
                        show_alert=True,
                    ),
                    cacheTime=1800,
                ),
            )
    logging.warning("Unknown callback action `%s` for #%s", action_id, callback_id)
    raise ErrorCustomBruhher(
        statusCode=status.HTTP_400_BAD_REQUEST,
        response=DefaultResponseModel(
            error=DefaultErrorModel(
                name="CALLBACK_ACTION_INVALID",
                description="No such callback action is available",
            ),
            result=None,
        ),
    )


@app.options(
    "/allowed",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_user_allowance(request: Request, user_id: int, allowed_status: bool):
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
        DB.set_user_allowance(int(user_id), allowed_status)
    except Exception as e:
        logging.error(e)
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
    if DB.get_user_allowed(int(user_id)):
        USER_ALLOWANCE = True
    return DefaultResponseModel(
        error=None,
        result=UserAllowanceResultModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=UserAllowedModel(allowed=USER_ALLOWANCE),
        ),
    )


@app.put(
    "/token",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_201_CREATED,
)
def create_token(request: Request, token_str: str):
    if not check_proper_headers(request, True):
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
        DB.create_token(
            DatabaseTokenObjectModel(
                token=token_str,
                totalUsage=0,
                lastUsage=None,
                allowed=True,
                maxUsage=None,
            ),
        )
    except Exception as e:
        logging.error(e)
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="DB_TOKEN_ERROR",
                    description="An error occurred while creating token",
                ),
                result=None,
            ),
        )
    return DefaultResponseModel(
        error=None,
        result=DatabaseTokenResponseOverallModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=DB.get_token(token_str),
        ),
    )


@app.options(
    "/token",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_token(
    request: Request,
    token_str: str,
    allowed: Optional[bool] = None,
    maxUsage: Optional[int] = None,
):
    if not check_proper_headers(request, True):
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
        DB.update_token(token_str, "allowed", allowed) if allowed else None
        DB.update_token(token_str, "maxUsage", maxUsage) if maxUsage else None
    except Exception as e:
        logging.error(e)
        raise ErrorCustomBruhher(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=DefaultResponseModel(
                error=DefaultErrorModel(
                    name="DB_TOKEN_ERROR",
                    description="An error occurred while updating token",
                ),
                result=None,
            ),
        )
    return DefaultResponseModel(
        error=None,
        result=DatabaseTokenResponseOverallModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=DB.get_token(token_str),
        ),
    )


@app.get(
    "/voices", response_model=VoiceListResponseModel, status_code=status.HTTP_200_OK,
)
def get_voices(v2_format: bool = False, sort_by: str = "voice"):
    if not v2_format and sort_by == "voice":
        return VoiceListResponseModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=[
                SpokenVoiceModel(
                    company=voice[0],
                    language=voice[1],
                    name=voice[2],
                    emotion=voice[3],
                    title=voice[4],
                )
                for voice in AVAILABLE_VOICES
            ],
        )
    elif v2_format and sort_by == "voice":
        voices = {}
        for voice in AVAILABLE_VOICES:
            if voice[2] not in voices:
                voices[voice[2]] = []
            voices[voice[2]].append(
                SpokenVoiceModel(
                    company=voice[0],
                    language=voice[1],
                    name=voice[2],
                    emotion=voice[3],
                    title=voice[4],
                ),
            )
        return VoiceListResponseModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=voices,
        )
    raise ErrorCustomBruhher(
        statusCode=status.HTTP_400_BAD_REQUEST,
        response=DefaultResponseModel(
            error=DefaultErrorModel(
                name="INVALID_VOICE_SORT",
                description="Invalid voice sort parameter",
            ),
            result=None,
        ),
    )
