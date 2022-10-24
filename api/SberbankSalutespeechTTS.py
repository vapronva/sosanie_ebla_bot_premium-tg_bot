from pathlib import Path
import requests
import os

_SSP_API_ENDPOINT = os.environ.get(
    "SBERBANK_SALUTESPEECH_ENDPOINTAPI",
    "https://mlspace.aicloud.sbercloud.ru/aicloud/ui/smartspeech/recognize/text",
)


class SberbankSaluteSpeechDemo:
    @staticmethod
    def synthesize(selectedVoice: str, text: str, output_file: Path) -> None:
        response = requests.post(
            url=f"{_SSP_API_ENDPOINT}?voice={selectedVoice.upper()}",
            json={"text": text},
        )
        response.raise_for_status()
        with open(output_file, "wb") as f:  # skipcq: PTC-W6004
            f.write(response.content)
