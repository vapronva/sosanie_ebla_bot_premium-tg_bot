import logging
import uuid
from pathlib import Path
from typing import List, Optional

import ffmpy
import sentry_sdk
import speechkit
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from requests import get as requests_get
from sentry_sdk.integrations.pymongo import (
    PyMongoIntegration as SentryPyMongoIntegration,
)
from speechkit.tts.synthesizer import AudioEncoding as SpeechKitAudioEncoding
from speechkit.tts.synthesizer import SynthesisConfig as SpeechKitSynthesisConfig
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from config import Config
from db import DB as DatabaseManager
from http_errors import (
    ERROR_CALLBACK_ACTION_INVALID,
    ERROR_CALLBACK_NOT_FOUND,
    ERROR_DB_TOKEN_ERROR,
    ERROR_DB_UPDATE_ERROR,
    ERROR_FILE_NOT_FOUND,
    ERROR_FORBIDDEN_BALLS,
    ERROR_INVALID_VOICE_SORT,
    ERROR_REQUEST_NOT_FOUND,
    ERROR_SBERBANK_TTS_ERROR,
    ERROR_TINKOFF_TTS_ERROR,
    ERROR_VKCV_TTS_ERROR,
    ERROR_VOICE_IRRETRIEVABLE,
    ERROR_VOICE_NOT_FOUND,
    ERROR_VOICE_PROVIDER_NOT_FOUND,
    ERROR_YANDEX_TTS_ERROR,
    ErrorCustomBruhher,
)
from models import (
    AdditionalDataModel,
    CallbackDataModel,
    CallbackResponseShowTextModel,
    CallbackShowTextModelResponseModel,
    DatabaseTokenObjectModel,
    DatabaseTokenResponseOverallModel,
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
from SberbankSalutespeechTTS import SberbankSaluteSpeechDemo
from TinkoffVoicekitTTS import process_text_to_speech as tinkoff_tts
from VKCloudVoiceTTS import VCVoices as VKCloudVoiceVoices
from VKCloudVoiceTTS import VKCloudVoiceTTS

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

CONFIG = Config()

sentry_sdk.init(
    dsn=CONFIG.get_sentry_dsn(),
    release=CONFIG.get_deployment_release(),
    environment=CONFIG.get_deployment_environment(),
    traces_sample_rate=1.0,
    enable_tracing=True,
    integrations=[
        SentryPyMongoIntegration(),
    ],
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
    ("yandex", "de", "lea", None, "Леа (обычная)"),
    ("yandex", "en", "john", None, "Джонн (обычный)"),
    ("yandex", "he", "naomi", "modern", "Наоми (современная)"),
    ("yandex", "he", "naomi", "classic", "Наоми (классическая)"),
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
    ("yandex", "ru", "dasha", None, "Даша (обычная)"),
    ("yandex", "ru", "julia", None, "Юлия (обычная)"),
    ("yandex", "ru", "lera", None, "Лера (обычная)"),
    ("yandex", "ru", "marina", None, "Марина (обычная)"),
    ("yandex", "ru", "alexander", None, "Александр (обычный)"),
    ("yandex", "ru", "kirill", None, "Кирилл (обычный)"),
    ("yandex", "ru", "anton", None, "Антон (обычный)"),
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
    ("sberbank", "en", "kira", None, "Кира (обычная)"),
]

app = FastAPI(
    debug=logging.DEBUG,  # type: ignore
    title="Sosanie Ebla Bot Premium API",
    version="0.3.0",
    contact={"email": CONFIG.get_api_contact_email()},
)

VCV_TTS = VKCloudVoiceTTS(CONFIG.get_vk_cloudvoice_servicetoken())

speechkit.configure_credentials(
    yandex_credentials=speechkit.creds.YandexCredentials(
        api_key=CONFIG.get_yandex_speechkit_apitoken(),
    ),
)


def check_proper_headers(
    request: Request,
    check_only_master_token: bool = False,
) -> bool:
    if request.headers.get("X-API-Token") != CONFIG.get_vprw_api_key():
        if (
            DB.check_token_usage(request.headers.get("X-API-Key") or "")
            and not check_only_master_token
        ):
            DB.update_token_usage(request.headers.get("X-API-Key") or "")
            return True
        logging.warning("Wrong API key detected in request for %s", request.url)
        return False
    return True


def check_proper_user_agent(request: Request) -> bool:
    return "TelegramBot" in request.headers.get("User-Agent").__str__()


@app.exception_handler(ErrorCustomBruhher)
def custom_error_bruhher(request: Request, exc: ErrorCustomBruhher) -> JSONResponse:
    return JSONResponse(
        status_code=exc.statusCode,
        content=exc.response.model_dump(mode="json"),
    )


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return DefaultResponseModel(error=None, result=None)


@app.get(
    "/allowed",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_200_OK,
)
def is_user_allowed(request: Request, user_id: int):
    if not check_proper_headers(request):
        raise ERROR_FORBIDDEN_BALLS
    USER_ALLOWANCE = bool(DB.get_user_allowed(user_id))
    return DefaultResponseModel(
        error=None,
        result=UserAllowanceResultModel(
            requestID=str(uuid.uuid4()),
            cacheTime=10,
            data=UserAllowedModel(allowed=USER_ALLOWANCE),
        ),
    )


def generate_selected_voice_tinkoff(additional_data: AdditionalDataModel) -> str:
    if additional_data.speakerEmotion:
        return f"{additional_data.speakerName}:{additional_data.speakerEmotion}"
    return additional_data.speakerName


@app.get("/tts/voice/{request_id}/{voice_id}.ogg", status_code=status.HTTP_200_OK)
def voice_message_server(request: Request, request_id: str, voice_id: str):
    user_request = DB.get_request(request_id=request_id)
    if not user_request:
        raise ERROR_REQUEST_NOT_FOUND
    selected_voice = next((x for x in user_request.tts if x.voice_id == voice_id), None)
    if not selected_voice:
        raise ERROR_VOICE_NOT_FOUND
    output_file = Path(f"./voice_messages_storage/{voice_id}.wav")
    if output_file.with_suffix(".ogg").exists():
        return FileResponse(output_file.with_suffix(".ogg"))
    if selected_voice.additionalData.company == "tinkoff":
        try:
            tinkoff_tts(
                text=user_request.content,
                selected_voice=generate_selected_voice_tinkoff(
                    selected_voice.additionalData,
                ),
                output_file=output_file,
            )
        except Exception as e:
            logging.error(e)
            raise ERROR_TINKOFF_TTS_ERROR from None
    elif selected_voice.additionalData.company == "yandex":
        try:
            model = speechkit.model_repository.synthesis_model()
            model.voice = generate_selected_voice_tinkoff(selected_voice.additionalData)
            model.sample_rate = 48000
            result: bytes = model.synthesize(
                text=user_request.content,
                synthesis_config=SpeechKitSynthesisConfig(
                    audio_encoding=SpeechKitAudioEncoding.WAV,
                    voice=generate_selected_voice_tinkoff(
                        selected_voice.additionalData,
                    ),
                ),
                raw_format=True,
            )
            output_file.write_bytes(result)
        except Exception as e:
            logging.error(e)
            raise ERROR_YANDEX_TTS_ERROR from None
    elif selected_voice.additionalData.company == "vk":
        try:
            VCV_TTS.save_audio(
                text=user_request.content,
                voice=VKCloudVoiceVoices(selected_voice.additionalData.speakerName),
                path=output_file.with_suffix(".mp3"),
            )
            ffmpy.FFmpeg(
                global_options="-y -loglevel quiet",
                inputs={str(output_file.with_suffix(".mp3")): None},
                outputs={
                    output_file.with_suffix(".wav")
                    .absolute()
                    .__str__(): "-acodec pcm_s16le -ac 1 -ar 24000",
                },
            ).run()
        except Exception as e:
            logging.error(e)
            raise ERROR_VKCV_TTS_ERROR from None
    elif selected_voice.additionalData.company == "sberbank":
        try:
            SberbankSaluteSpeechDemo.synthesize(
                selectedVoice=selected_voice.additionalData.speakerName,
                text=user_request.content,
                outputFile=output_file,
            )
        except Exception as e:
            logging.error(e)
            raise ERROR_SBERBANK_TTS_ERROR from None
    if not output_file.exists():
        raise ERROR_VOICE_PROVIDER_NOT_FOUND
    ffmpy.FFmpeg(
        global_options="-y -loglevel quiet",
        inputs={str(output_file): None},
        outputs={
            output_file.with_suffix(".ogg")
            .absolute()
            .__str__(): "-acodec libopus -ac 1 -ar 48000 -b:a 128k -vbr off",
        },
    ).run()
    return FileResponse(output_file.with_suffix(".ogg"))


@app.get("/tts/voice/{request_id}/{voice_id}.wav", status_code=status.HTTP_200_OK)
def voice_message_wav(
    request: Request,
    request_id: str,
    voice_id: str,
    download: bool = False,
):
    user_request = DB.get_request(request_id=request_id)
    if not user_request:
        raise ERROR_REQUEST_NOT_FOUND
    selected_voice = next((x for x in user_request.tts if x.voice_id == voice_id), None)
    if not selected_voice:
        raise ERROR_VOICE_NOT_FOUND
    output_file = Path(f"./voice_messages_storage/{voice_id}.wav")
    if not output_file.exists():
        _ = requests_get(
            url=f"http://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.ogg",
            timeout=25,
        )
    if output_file.exists():
        if download:
            return FileResponse(
                output_file,
                media_type="audio/wav",
                headers={
                    "Content-Disposition": f"attachment, filename=sosanieeblabotpremium-{voice_id.replace('-', '')}.wav",
                },
            )
        return FileResponse(output_file)
    if output_file.with_suffix(".ogg").exists() and not output_file.exists():
        raise ERROR_VOICE_IRRETRIEVABLE
    raise ERROR_FILE_NOT_FOUND


@app.post(
    "/tts/request",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_201_CREATED,
)
def request_tts(request: Request, body: TTSRequestBodyModel):
    request_id = str(uuid.uuid4())
    if not check_proper_headers(request):
        raise ERROR_FORBIDDEN_BALLS
    tts_messages: List[VoiceMessageTTSInlineModel] = []
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
        tts_messages.append(
            VoiceMessageTTSInlineModel(
                url=f"http://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.ogg",
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
                    getVoiceTextID=f"{request_id[-12:]}-{uuid.uuid4().__str__().replace('-', '_')}",
                    publicVoiceWavUrl=f"http://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.wav?download=true",
                ),
            ),
        )
    DB.create_user_content(
        UserRequestContentDatabaseModel(
            user_id=body.user_id,
            content=body.query,
            requestID=request_id,
            tts=tts_messages,
        ),
    )
    return DefaultResponseModel(
        error=None,
        result=VoiceMessagesTTSResultModel(
            requestID=request_id,
            cacheTime=10,
            data=tts_messages,
        ),
    )


@app.post(
    "/tts/request/wav",
    status_code=status.HTTP_201_CREATED,
)
def request_tts_wav(request: Request, body: TTSRequestWithDirectWavBodyModel):
    request_id = str(uuid.uuid4())
    if not check_proper_headers(request):
        raise ERROR_FORBIDDEN_BALLS
    tts_messages: List[VoiceMessageTTSInlineModel] = []
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
        tts_messages.append(
            VoiceMessageTTSInlineModel(
                url=f"http://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.ogg",
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
                    getVoiceTextID=f"{request_id[-12:]}-{uuid.uuid4().__str__().replace('-', '_')}",
                    publicVoiceWavUrl=f"http://{CONFIG.get_vprw_api_endpoint()}/tts/voice/{request_id}/{voice_id}.wav",
                ),
            ),
        )
    DB.create_user_content(
        UserRequestContentDatabaseModel(
            user_id=body.user_id,
            content=body.query,
            requestID=request_id,
            tts=tts_messages,
        ),
    )
    if not tts_messages:
        raise ERROR_VOICE_PROVIDER_NOT_FOUND
    return Response(
        str(
            f"{tts_messages[0].callbackData.publicVoiceWavUrl}"
            if tts_messages[0].callbackData is not None
            else f"{tts_messages[0].url}",
        ),
        status_code=status.HTTP_201_CREATED,
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=sosanieeblabotpremium-{tts_messages[0].voice_id.replace('-', '')}.wav",
        },
    )


@app.get("/callback/action/{action_id}/{callback_id}", status_code=status.HTTP_200_OK)
def answer_callback_action_sucktion(request: Request, action_id: str, callback_id: str):
    if not check_proper_headers(request):
        raise ERROR_FORBIDDEN_BALLS
    logging.info("Received callback action `%s` for #%s", action_id, callback_id)
    match action_id:
        case "getshwsgt":
            user_request = DB.get_request_by_callback_data(
                "getVoiceTextID",
                callback_id,
            )
            if not user_request:
                raise ERROR_CALLBACK_NOT_FOUND
            logging.info(
                "Sending text for #%s as of request #%s",
                callback_id,
                user_request.requestID,
            )
            return DefaultResponseModel(
                error=None,
                result=CallbackShowTextModelResponseModel(
                    requestID=str(uuid.uuid4()),
                    data=CallbackResponseShowTextModel(
                        text=f'Original text: "{user_request.content}"',
                        show_alert=True,
                    ),
                    cacheTime=1800,
                ),
            )
    logging.warning("Unknown callback action `%s` for #%s", action_id, callback_id)
    raise ERROR_CALLBACK_ACTION_INVALID


@app.options(
    "/allowed",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_202_ACCEPTED,
)
def change_user_allowance(request: Request, user_id: int, allowed_status: bool):
    if not check_proper_headers(request):
        raise ERROR_FORBIDDEN_BALLS
    try:
        DB.set_user_allowance(user_id, allowed_status)
    except Exception as e:
        logging.error(e)
        raise ERROR_DB_UPDATE_ERROR from None
    USER_ALLOWANCE = bool(DB.get_user_allowed(user_id))
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
        raise ERROR_FORBIDDEN_BALLS
    try:
        DB.create_token(
            DatabaseTokenObjectModel(
                token=token_str,
                lastUsage=None,
                allowed=True,
                maxUsage=None,
                used=0,
            ),
        )
    except Exception as e:
        logging.error(e)
        raise ERROR_DB_TOKEN_ERROR from None
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
    max_usage: Optional[int] = None,
):
    if not check_proper_headers(request, True):
        raise ERROR_FORBIDDEN_BALLS
    try:
        DB.update_token(token_str, "allowed", allowed) if allowed else None
        DB.update_token(token_str, "maxUsage", max_usage) if max_usage else None
    except Exception as e:
        logging.error(e)
        raise ERROR_DB_TOKEN_ERROR from None
    return DefaultResponseModel(
        error=None,
        result=DatabaseTokenResponseOverallModel(
            requestID=str(uuid.uuid4()),
            cacheTime=60,
            data=DB.get_token(token_str),
        ),
    )


@app.get(
    "/voices",
    response_model=VoiceListResponseModel,
    status_code=status.HTTP_200_OK,
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
    raise ERROR_INVALID_VOICE_SORT
