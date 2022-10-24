from typing import Optional, Tuple
from tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2
from tinkoff.auth import authorization_metadata
import grpc
import os
import wave
from pathlib import Path

_VKC_API_ENDPOINT = os.environ.get("TINKOFF_VOICEKIT_ENDPOINTAPI", "api.tinkoff.ai:443")
_VCK_API_KEY = os.environ["TINKOFF_VOICEKIT_APIKEY"]
_VCK_SECRET_KEY = os.environ["TINKOFF_VOICEKIT_SECRETKEY"]

SAMPLE_RATE = 48000


def process_text_to_speech(
    text: str,
    selected_voice: str,
    output_file: Path,
    sample_rate: int = SAMPLE_RATE,
    api_key: str = _VCK_API_KEY,
    secret_key: str = _VCK_SECRET_KEY,
    endpoint_api: str = _VKC_API_ENDPOINT,
) -> Tuple[Optional[float]]:
    request = tts_pb2.SynthesizeSpeechRequest(
        input=tts_pb2.SynthesisInput(
            text=text,
        ),
        voice=tts_pb2.VoiceSelectionParams(
            name=selected_voice,
        ),
        audio_config=tts_pb2.AudioConfig(
            audio_encoding=tts_pb2.LINEAR16,
            sample_rate_hertz=sample_rate,
        ),
    )
    with wave.open(output_file.absolute().__str__(), mode="wb") as f:
        f.setframerate(sample_rate)
        f.setnchannels(1)
        f.setsampwidth(2)
        stub = tts_pb2_grpc.TextToSpeechStub(
            grpc.secure_channel(endpoint_api, grpc.ssl_channel_credentials())
        )
        metadata = authorization_metadata(api_key, secret_key, "tinkoff.cloud.tts")
        responses = stub.StreamingSynthesize(request, metadata=metadata)
        AUDIO_DURATION = None
        for key, value in responses.initial_metadata():
            if key == "x-audio-duration-seconds":
                AUDIO_DURATION = float(value)
                break
        for stream_response in responses:
            f.writeframes(stream_response.audio_chunk)
    return (AUDIO_DURATION,)
