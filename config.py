import os

_REQUIRED_FIELDS = [
    "TINKOFF_VOICEKIT_APIKEY",
    "TINKOFF_VOICEKIT_SECRETKEY",
    "TINKOFF_VOICEKIT_ENDPOINTAPI",
    "TELEGRAM_API_ID",
    "TELEGRAM_API_HASH",
    "TELEGRAM_BOT_TOKEN",
]


class Config:
    def __init__(self) -> None:
        self.__check_env_vars()

    @staticmethod
    def __check_env_vars():
        for field in _REQUIRED_FIELDS:
            if field not in os.environ:
                raise ValueError(f"Environment variable {field} is not set")

    @staticmethod
    def __get_env_var(name: str) -> str:
        if name not in os.environ:
            raise ValueError(f"Environment variable {name} is not set")
        return os.environ[name]

    def get_tinkoff_voicekit_apikey(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_APIKEY")

    def get_tinkoff_voicekit_secretkey(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_SECRETKEY")

    def get_tinkoff_voicekit_endpointapi(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_ENDPOINTAPI")

    def get_telegram_api_id(self) -> str:
        return self.__get_env_var("TELEGRAM_API_ID")

    def get_telegram_api_hash(self) -> str:
        return self.__get_env_var("TELEGRAM_API_HASH")

    def get_telegram_bot_token(self) -> str:
        return self.__get_env_var("TELEGRAM_BOT_TOKEN")
