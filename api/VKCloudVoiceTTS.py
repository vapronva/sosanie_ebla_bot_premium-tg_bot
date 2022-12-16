from pathlib import Path
import requests
import os
from enum import Enum

_VCV_API_ENDPOINT = os.environ.get(
    "VK_CLOUDVOICE_ENDPOINTAPI",
    "https://voice.mcs.mail.ru/tts",
)


class VCVoices(str, Enum):
    KATHERINE = "katherine"
    KATHERINE_HIFIGAN = "katherine-hifigan"
    MARIA = "maria"
    MARIA_SERIOUS = "maria-serious"
    PAVEL = "pavel"
    PAVEL_HIFIGAN = "pavel-hifigan"


class AvailableFormats(str, Enum):
    PCM = "pcm"
    MP3 = "mp3"
    OPUS = "opus"


class VKCloudVoiceTTS:
    def __init__(self, serviceToken: str) -> None:
        self.__SERVICE_TOKEN = serviceToken

    def __get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.__SERVICE_TOKEN}",
        }

    def __request(
        self,
        text: str,
        voice: VCVoices,
        format: AvailableFormats = AvailableFormats.MP3,
        speed: float = 1.0,
    ) -> requests.Response:
        return requests.get(
            _VCV_API_ENDPOINT,
            headers=self.__get_headers(),
            params={
                "text": text,
                "model_name": voice.value,
                "encoder": format.value,
                "tempo": str(speed),
            },
        )

    def get_audio(
        self,
        text: str,
        voice: VCVoices,
        format: AvailableFormats = AvailableFormats.MP3,
        speed: float = 1.0,
    ) -> bytes:
        return self.__request(text, voice, format, speed).content

    def save_audio(
        self,
        text: str,
        voice: VCVoices,
        path: Path,
        format: AvailableFormats = AvailableFormats.MP3,
        speed: float = 1.0,
    ) -> None:
        with open(path, "wb") as f:
            f.write(self.get_audio(text, voice, format, speed))
