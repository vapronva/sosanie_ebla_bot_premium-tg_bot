import os

_REQUIRED_FIELDS = [
    "TINKOFF_VOICEKIT_APIKEY",
    "TINKOFF_VOICEKIT_SECRETKEY",
    "TINKOFF_VOICEKIT_ENDPOINTAPI",
    "VPRW_API_KEY",
    "VPRW_API_ENDPOINT",
    "API_CONTACT_EMAIL",
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

    def get_vprw_api_key(self) -> str:
        return self.__get_env_var("VPRW_API_KEY")

    def get_vprw_api_endpoint(self) -> str:
        return self.__get_env_var("VPRW_API_ENDPOINT")

    def get_api_contact_email(self) -> str:
        return self.__get_env_var("API_CONTACT_EMAIL")
