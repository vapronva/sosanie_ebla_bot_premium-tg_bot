from typing import Optional, Union
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
    speakerEmotion: str


class VoiceMessageTTSInlineModel(BaseModel):
    url: HttpUrl
    title: str
    caption: Optional[str]
    additionalData: Optional[AdditionalDataModel]


class VoiceMessagesTTSResultModel(DefaultResultModel):
    data: list[VoiceMessageTTSInlineModel]


class DefaultResponseModel(BaseModel):
    error: Optional[DefaultErrorModel]
    result: Optional[DefaultResultModel]
