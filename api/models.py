from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl, NonNegativeInt
from datetime import datetime


class DefaultErrorModel(BaseModel):
    name: str
    description: str


class DefaultResultModel(BaseModel):
    requestID: str
    cacheTime: int
    data: Union[list, dict]


class AdditionalDataModel(BaseModel):
    speakerLang: str
    speakerName: str
    speakerEmotion: Optional[str]
    company: str


class CallbackDataModel(BaseModel):
    getVoiceTextID: str
    publicVoiceWavUrl: HttpUrl | None = None


class VoiceMessageTTSInlineModel(BaseModel):
    url: HttpUrl
    title: str
    caption: Optional[str]
    voice_id: str
    additionalData: AdditionalDataModel
    callbackData: Optional[CallbackDataModel]


class VoiceMessagesTTSResultModel(DefaultResultModel):
    data: list[VoiceMessageTTSInlineModel]


class DefaultResponseModel(BaseModel):
    error: Optional[DefaultErrorModel]
    result: Optional[DefaultResultModel]


class TTSRequestModel(BaseModel):
    user_id: int
    query: str


class UserAllowedModel(BaseModel):
    allowed: bool


class UserAllowanceResultModel(DefaultResultModel):
    data: UserAllowedModel


class TTSRequestBodyModel(BaseModel):
    user_id: int
    query: str


class TTSRequestWithDirectWavBodyModel(BaseModel):
    user_id: int
    query: str
    voice: AdditionalDataModel


class UserRequestContentDatabaseModel(BaseModel):
    user_id: int
    requestID: str
    content: str
    tts: List[VoiceMessageTTSInlineModel]


class CallbackResponseShowTextModel(BaseModel):
    text: str
    show_alert: bool


class CallbackShowTextModelResponseModel(DefaultResultModel):
    data: CallbackResponseShowTextModel


class DatabaseTokenObjectModel(BaseModel):
    token: str
    totalUsage: NonNegativeInt
    lastUsage: Optional[datetime]
    allowed: bool
    maxUsage: Optional[NonNegativeInt]


class DatabaseTokenResponseOverallModel(DefaultResultModel):
    data: Optional[DatabaseTokenObjectModel]
