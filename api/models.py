from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl


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


class UserRequestContentDatabaseModel(BaseModel):
    user_id: int
    requestID: str
    content: str
    tts: List[VoiceMessageTTSInlineModel]
