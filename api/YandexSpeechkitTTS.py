from pathlib import Path
from typing import Optional
import requests
from enum import Enum


class APIEndpoints(str, Enum):
    Text2Speech: str = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    IAM: str = "https://iam.api.cloud.yandex.net/iam/v1/tokens"


class YandexTTS:
    __voicesList = [
        {"name": "lea", "language": "de-DE", "gender": "female"},
        {"name": "john", "language": "en-US", "gender": "male"},
        {"name": "amira", "language": "kk-KK", "gender": "female"},
        {"name": "madi", "language": "kk-KK", "gender": "male"},
        {"name": "alena", "language": "ru-RU", "gender": "female"},
        {"name": "filipp", "language": "ru-RU", "gender": "male"},
        {"name": "ermil", "language": "ru-RU", "gender": "male"},
        {"name": "jane", "language": "ru-RU", "gender": "female"},
        {"name": "madirus", "language": "ru-RU", "gender": "male"},
        {"name": "omazh", "language": "ru-RU", "gender": "female"},
        {"name": "zahar", "language": "ru-RU", "gender": "male"},
        {"name": "nigora", "language": "uz-UZ", "gender": "female"},
    ]

    def __init__(
        self,
        voice: str,
        emotion: Optional[str],
        speed: float,
        audioFormat: str,
        sampleRateHertz: int,
        folderId: str,
        maxCharachters: int = 5000,
    ) -> None:
        self._maxCharachters = maxCharachters
        if voice not in map(lambda d: d["name"], self.__voicesList):
            raise TypeError("Invalid speaker: no such a speaker was found in a list.")
        self._params = {
            "lang": next(  # skipcq: PTC-W0063
                item for item in self.__voicesList if item["name"] == voice
            )["language"],
            "voice": voice,
            "speed": speed,
            "format": audioFormat,
            "sampleRateHertz": sampleRateHertz,
            "folderId": folderId,
        }
        if emotion:
            self._params["emotion"] = emotion
        self.__data = None

    def IAMGen(self, ycAPIKey: str) -> None:
        self._IAMToken = ycAPIKey  # skipcq: PYL-W0201

    def generate(self, text: str) -> None:
        if len(text) >= self._maxCharachters:
            raise ValueError(
                f"Too many charchters: number of characters must be less than {self._maxCharachters}"
            )
        params = self._params.copy()
        params["text"] = text
        self.__data = requests.post(
            APIEndpoints.Text2Speech.value,
            headers={"Authorization": f"Api-Key {self._IAMToken}"},
            data=params,
            stream=True,
        ).iter_content()

    def writeData(self, path: Path) -> None:
        with open(path, "wb") as f:  # skipcq: PTC-W6004
            for data in self.__data:  # type: ignore
                f.write(data)

    def getData(self) -> bytes:
        bytes_data = b""
        for data in self.__data:  # type: ignore
            bytes_data += data
        return bytes_data
