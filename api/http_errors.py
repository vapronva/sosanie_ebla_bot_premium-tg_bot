from fastapi import status

from models import DefaultErrorModel, DefaultResponseModel


class ErrorCustomBruhher(Exception):
    def __init__(
        self,
        response: DefaultResponseModel,
        status_code: int,
    ) -> None:
        self.response = response
        self.statusCode = status_code


ERROR_FORBIDDEN_BALLS = ErrorCustomBruhher(
    status_code=status.HTTP_403_FORBIDDEN,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="FORBIDDEN_BALLS",
            description="You are not authorized to access this resource",
        ),
        result=None,
    ),
)

ERROR_REQUEST_NOT_FOUND = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="REQUEST_NOT_FOUND",
            description="No such request found in database or it has expired",
        ),
        result=None,
    ),
)

ERROR_VOICE_NOT_FOUND = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="VOICE_NOT_FOUND",
            description="No such voice message found in the request",
        ),
        result=None,
    ),
)

ERROR_TINKOFF_TTS_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="TINKOFF_TTS_ERROR",
            description="Tinkoff TTS service is unavailable at the moment",
        ),
        result=None,
    ),
)

ERROR_YANDEX_TTS_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="YANDEX_TTS_ERROR",
            description="Yandex TTS service is unavailable at the moment",
        ),
        result=None,
    ),
)

ERROR_VKCV_TTS_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="VKCV_TTS_ERROR",
            description="VK TTS service is unavailable at the moment",
        ),
        result=None,
    ),
)

ERROR_SBERBANK_TTS_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="SBERBANK_TTS_ERROR",
            description="SberBank TTS service is unavailable at the moment",
        ),
        result=None,
    ),
)

ERROR_VOICE_IRRETRIEVABLE = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="VOICE_IRRETRIEVABLE",
            description="Voice message is not available in .wav format",
        ),
        result=None,
    ),
)

ERROR_VOICE_PROVIDER_NOT_FOUND = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="VOICE_PROVIDER_NOT_FOUND",
            description="No such voice provider found in available TTS models",
        ),
        result=None,
    ),
)

ERROR_CALLBACK_ACTION_INVALID = ErrorCustomBruhher(
    status_code=status.HTTP_400_BAD_REQUEST,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="CALLBACK_ACTION_INVALID",
            description="No such callback action is available",
        ),
        result=None,
    ),
)

ERROR_CALLBACK_NOT_FOUND = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="CALLBACK_NOT_FOUND",
            description="No such callback found in database",
        ),
        result=None,
    ),
)

ERROR_DB_UPDATE_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="DB_UPDATE_ERROR",
            description="An error occurred while updating user's allowance status",
        ),
        result=None,
    ),
)

ERROR_DB_TOKEN_ERROR = ErrorCustomBruhher(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="DB_TOKEN_ERROR",
            description="An error occurred while creating token",
        ),
        result=None,
    ),
)

ERROR_INVALID_VOICE_SORT = ErrorCustomBruhher(
    status_code=status.HTTP_400_BAD_REQUEST,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="INVALID_VOICE_SORT",
            description="Invalid voice sort parameter",
        ),
        result=None,
    ),
)

ERROR_FILE_NOT_FOUND = ErrorCustomBruhher(
    status_code=status.HTTP_404_NOT_FOUND,
    response=DefaultResponseModel(
        error=DefaultErrorModel(
            name="FILE_NOT_FOUND",
            description="No such file found in the storage",
        ),
        result=None,
    ),
)
