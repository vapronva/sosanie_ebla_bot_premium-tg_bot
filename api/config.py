import os

_REQUIRED_FIELDS = [
    "TINKOFF_VOICEKIT_APIKEY",
    "TINKOFF_VOICEKIT_SECRETKEY",
    "TINKOFF_VOICEKIT_ENDPOINTAPI",
    "YANDEX_SPEECHKIT_FOLDERID",
    "YANDEX_SPEECHKIT_APITOKEN",
    "VK_CLOUDVOICE_ENDPOINTAPI",
    "VK_CLOUDVOICE_SERVICETOKEN",
    "SBERBANK_SALUTESPEECH_ENDPOINTAPI",
    "VPRW_API_KEY",
    "VPRW_API_ENDPOINT",
    "API_CONTACT_EMAIL",
    "DB_MONGODB_URI",
    "SENTRY_DSN",
    "DEPLOYMENT_ENVIRONMENT",
]


class Config:
    def __init__(self) -> None:
        self.__check_env_vars()

    @staticmethod
    def __check_env_vars():
        for field in _REQUIRED_FIELDS:
            if field not in os.environ:
                msg = f"Environment variable {field} is not set"
                raise ValueError(msg)

    @staticmethod
    def __get_env_var(name: str) -> str:
        if name not in os.environ:
            msg = f"Environment variable {name} is not set"
            raise ValueError(msg)
        return os.environ[name]

    def get_tinkoff_voicekit_apikey(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_APIKEY")

    def get_tinkoff_voicekit_secretkey(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_SECRETKEY")

    def get_tinkoff_voicekit_endpointapi(self) -> str:
        return self.__get_env_var("TINKOFF_VOICEKIT_ENDPOINTAPI")

    def get_yandex_speechkit_folderid(self) -> str:
        return self.__get_env_var("YANDEX_SPEECHKIT_FOLDERID")

    def get_yandex_speechkit_apitoken(self) -> str:
        return self.__get_env_var("YANDEX_SPEECHKIT_APITOKEN")

    def get_vk_cloudvoice_endpointapi(self) -> str:
        return self.__get_env_var("VK_CLOUDVOICE_ENDPOINTAPI")

    def get_vk_cloudvoice_servicetoken(self) -> str:
        return self.__get_env_var("VK_CLOUDVOICE_SERVICETOKEN")

    def get_sberbank_salutespeech_endpointapi(self) -> str:
        return self.__get_env_var("SBERBANK_SALUTESPEECH_ENDPOINTAPI")

    def get_vprw_api_key(self) -> str:
        return self.__get_env_var("VPRW_API_KEY")

    def get_vprw_api_endpoint(self) -> str:
        return self.__get_env_var("VPRW_API_ENDPOINT")

    def get_api_contact_email(self) -> str:
        return self.__get_env_var("API_CONTACT_EMAIL")

    def get_db_mongodb_uri(self) -> str:
        return self.__get_env_var("DB_MONGODB_URI")

    def get_sentry_dsn(self) -> str:
        return self.__get_env_var("SENTRY_DSN")

    def get_deployment_release(self) -> str:
        with open("VERSION") as f:
            return f.read().strip()

    def get_deployment_environment(self) -> str:
        return self.__get_env_var("DEPLOYMENT_ENVIRONMENT")
