"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()

from google.api import (
    annotations_pb2 as google_dot_api_dot_annotations__pb2,  # skipcq: PY-W2000
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1etinkoff/cloud/tts/v1/tts.proto\x12\x14tinkoff.cloud.tts.v1\x1a\x1cgoogle/api/annotations.proto"_\n\x05Voice\x12\x0c\n\x04name\x18\x02 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05R\x0elanguage_codesR\x0bssml_genderR\x19natural_sample_rate_hertz"(\n\x11ListVoicesRequestJ\x04\x08\x01\x10\x02R\rlanguage_code"B\n\x13ListVoicesResponses\x12+\n\x06voices\x18\x01 \x03(\x0b\x32\x1b.tinkoff.cloud.tts.v1.Voice",\n\x0eSynthesisInput\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0c\n\x04ssml\x18\x02 \x01(\t"L\n\x14VoiceSelectionParams\x12\x0c\n\x04name\x18\x02 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x03\x10\x04R\rlanguage_codeR\x0bssml_gender"\x9d\x01\n\x0b\x41udioConfig\x12;\n\x0e\x61udio_encoding\x18\x01 \x01(\x0e\x32#.tinkoff.cloud.tts.v1.AudioEncoding\x12\x19\n\x11sample_rate_hertz\x18\x05 \x01(\x05J\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05R\rspeaking_rateR\x05pitchR\x0evolume_gain_db"\xc2\x01\n\x17SynthesizeSpeechRequest\x12\x33\n\x05input\x18\x01 \x01(\x0b\x32$.tinkoff.cloud.tts.v1.SynthesisInput\x12\x39\n\x05voice\x18\x02 \x01(\x0b\x32*.tinkoff.cloud.tts.v1.VoiceSelectionParams\x12\x37\n\x0c\x61udio_config\x18\x03 \x01(\x0b\x32!.tinkoff.cloud.tts.v1.AudioConfig"1\n\x18SynthesizeSpeechResponse\x12\x15\n\raudio_content\x18\x01 \x01(\x0c"8\n!StreamingSynthesizeSpeechResponse\x12\x13\n\x0b\x61udio_chunk\x18\x01 \x01(\x0c*\xe4\x01\n\rAudioEncoding\x12\x18\n\x14\x45NCODING_UNSPECIFIED\x10\x00\x12\x0c\n\x08LINEAR16\x10\x01\x12\x08\n\x04\x41LAW\x10\x08\x12\x0c\n\x08RAW_OPUS\x10\x0b"\x04\x08\x02\x10\x02"\x04\x08\x03\x10\x03"\x04\x08\x04\x10\x04"\x04\x08\x05\x10\x05"\x04\x08\x06\x10\x06"\x04\x08\x07\x10\x07"\x04\x08\t\x10\t"\x04\x08\n\x10\n"\x04\x08\x0c\x10\x0c*\x04\x46LAC*\x05MULAW*\x03\x41MR*\x06\x41MR_WB*\x08OGG_OPUS*\x16SPEEX_WITH_HEADER_BYTE*\tLINEAR32F*\nOGG_VORBIS*\nMPEG_AUDIO2\x9b\x03\n\x0cTextToSpeech\x12}\n\nListVoices\x12\'.tinkoff.cloud.tts.v1.ListVoicesRequest\x1a).tinkoff.cloud.tts.v1.ListVoicesResponses"\x1b\x82\xd3\xe4\x93\x02\x15\x12\x13/v1/tts:list_voices\x12\x8a\x01\n\nSynthesize\x12-.tinkoff.cloud.tts.v1.SynthesizeSpeechRequest\x1a..tinkoff.cloud.tts.v1.SynthesizeSpeechResponse"\x1d\x82\xd3\xe4\x93\x02\x17"\x12/v1/tts:synthesize:\x01*\x12\x7f\n\x13StreamingSynthesize\x12-.tinkoff.cloud.tts.v1.SynthesizeSpeechRequest\x1a\x37.tinkoff.cloud.tts.v1.StreamingSynthesizeSpeechResponse0\x01\x42NZDgithub.com/Tinkoff/voicekit-examples/golang/pkg/tinkoff/cloud/tts/v1\xa2\x02\x05TVKSSb\x06proto3'
)

_AUDIOENCODING = DESCRIPTOR.enum_types_by_name["AudioEncoding"]
AudioEncoding = enum_type_wrapper.EnumTypeWrapper(_AUDIOENCODING)
ENCODING_UNSPECIFIED = 0
LINEAR16 = 1
ALAW = 8
RAW_OPUS = 11


_VOICE = DESCRIPTOR.message_types_by_name["Voice"]
_LISTVOICESREQUEST = DESCRIPTOR.message_types_by_name["ListVoicesRequest"]
_LISTVOICESRESPONSES = DESCRIPTOR.message_types_by_name["ListVoicesResponses"]
_SYNTHESISINPUT = DESCRIPTOR.message_types_by_name["SynthesisInput"]
_VOICESELECTIONPARAMS = DESCRIPTOR.message_types_by_name["VoiceSelectionParams"]
_AUDIOCONFIG = DESCRIPTOR.message_types_by_name["AudioConfig"]
_SYNTHESIZESPEECHREQUEST = DESCRIPTOR.message_types_by_name["SynthesizeSpeechRequest"]
_SYNTHESIZESPEECHRESPONSE = DESCRIPTOR.message_types_by_name["SynthesizeSpeechResponse"]
_STREAMINGSYNTHESIZESPEECHRESPONSE = DESCRIPTOR.message_types_by_name[
    "StreamingSynthesizeSpeechResponse"
]

Voice = _reflection.GeneratedProtocolMessageType(
    "Voice",
    (_message.Message,),
    {"DESCRIPTOR": _VOICE, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(Voice)

ListVoicesRequest = _reflection.GeneratedProtocolMessageType(
    "ListVoicesRequest",
    (_message.Message,),
    {"DESCRIPTOR": _LISTVOICESREQUEST, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(ListVoicesRequest)

ListVoicesResponses = _reflection.GeneratedProtocolMessageType(
    "ListVoicesResponses",
    (_message.Message,),
    {"DESCRIPTOR": _LISTVOICESRESPONSES, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(ListVoicesResponses)

SynthesisInput = _reflection.GeneratedProtocolMessageType(
    "SynthesisInput",
    (_message.Message,),
    {"DESCRIPTOR": _SYNTHESISINPUT, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(SynthesisInput)

VoiceSelectionParams = _reflection.GeneratedProtocolMessageType(
    "VoiceSelectionParams",
    (_message.Message,),
    {"DESCRIPTOR": _VOICESELECTIONPARAMS, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(VoiceSelectionParams)

AudioConfig = _reflection.GeneratedProtocolMessageType(
    "AudioConfig",
    (_message.Message,),
    {"DESCRIPTOR": _AUDIOCONFIG, "__module__": "tinkoff.cloud.tts.v1.tts_pb2"},
)
_sym_db.RegisterMessage(AudioConfig)

SynthesizeSpeechRequest = _reflection.GeneratedProtocolMessageType(
    "SynthesizeSpeechRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _SYNTHESIZESPEECHREQUEST,
        "__module__": "tinkoff.cloud.tts.v1.tts_pb2",
    },
)
_sym_db.RegisterMessage(SynthesizeSpeechRequest)

SynthesizeSpeechResponse = _reflection.GeneratedProtocolMessageType(
    "SynthesizeSpeechResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _SYNTHESIZESPEECHRESPONSE,
        "__module__": "tinkoff.cloud.tts.v1.tts_pb2",
    },
)
_sym_db.RegisterMessage(SynthesizeSpeechResponse)

StreamingSynthesizeSpeechResponse = _reflection.GeneratedProtocolMessageType(
    "StreamingSynthesizeSpeechResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _STREAMINGSYNTHESIZESPEECHRESPONSE,
        "__module__": "tinkoff.cloud.tts.v1.tts_pb2",
    },
)
_sym_db.RegisterMessage(StreamingSynthesizeSpeechResponse)

_TEXTTOSPEECH = DESCRIPTOR.services_by_name["TextToSpeech"]

if _descriptor._USE_C_DESCRIPTORS is False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"ZDgithub.com/Tinkoff/voicekit-examples/golang/pkg/tinkoff/cloud/tts/v1\242\002\005TVKSS"
    _TEXTTOSPEECH.methods_by_name["ListVoices"]._options = None
    _TEXTTOSPEECH.methods_by_name[
        "ListVoices"
    ]._serialized_options = b"\202\323\344\223\002\025\022\023/v1/tts:list_voices"
    _TEXTTOSPEECH.methods_by_name["Synthesize"]._options = None
    _TEXTTOSPEECH.methods_by_name[
        "Synthesize"
    ]._serialized_options = b'\202\323\344\223\002\027"\022/v1/tts:synthesize:\001*'
    _AUDIOENCODING._serialized_start = 884
    _AUDIOENCODING._serialized_end = 1112
    _VOICE._serialized_start = 86
    _VOICE._serialized_end = 181
    _LISTVOICESREQUEST._serialized_start = 183
    _LISTVOICESREQUEST._serialized_end = 223
    _LISTVOICESRESPONSES._serialized_start = 225
    _LISTVOICESRESPONSES._serialized_end = 291
    _SYNTHESISINPUT._serialized_start = 293
    _SYNTHESISINPUT._serialized_end = 337
    _VOICESELECTIONPARAMS._serialized_start = 339
    _VOICESELECTIONPARAMS._serialized_end = 415
    _AUDIOCONFIG._serialized_start = 418
    _AUDIOCONFIG._serialized_end = 575
    _SYNTHESIZESPEECHREQUEST._serialized_start = 578
    _SYNTHESIZESPEECHREQUEST._serialized_end = 772
    _SYNTHESIZESPEECHRESPONSE._serialized_start = 774
    _SYNTHESIZESPEECHRESPONSE._serialized_end = 823
    _STREAMINGSYNTHESIZESPEECHRESPONSE._serialized_start = 825
    _STREAMINGSYNTHESIZESPEECHRESPONSE._serialized_end = 881
    _TEXTTOSPEECH._serialized_start = 1115
    _TEXTTOSPEECH._serialized_end = 1526
